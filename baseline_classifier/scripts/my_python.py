import sys

from ntpath import basename
import os
import re
import subprocess
import h5py
import numpy as np
os.environ['THEANO_FLAGS'] = "device=gpu"
os.environ['floatX'] = 'float32'
from keras import regularizers
from keras.optimizers import SGD
from keras.models import Model, Sequential
from keras.layers import Conv1D, MaxPooling1D, Input, Flatten, Reshape, Activation, Dense
from keras.layers.merge import concatenate

def getFilename(string):
	return '.'.join(basename(string).split('.')[:-1])

def printHDF5(string):
	cmd = 'h5dump -A -H ' + string
	os.system(cmd)
def myOsSystem(cmd, debug):
	if debug is False:
		os.system(cmd)
		# print(cmd)
	else:
		print(cmd)
def mySubprocess(cmd, debug):
	if debug is False:
		result = subprocess.check_output(cmd, shell=True)
		return result
	else:
		print(cmd)
def getData(hdf5file, name):
	f = h5py.File(hdf5file, 'r')
	temp = f[name][()]
	f.close()
	return temp
def saveData(hdf5file, name, data):
	f = h5py.File(hdf5file, 'w')
	f.create_dataset(name, data=data)
	f.close()

# unique for this task
def read_motif_from_jaspar(filename, background_freq, alphabet_order):
	counter = 0
	pseudocount = 1e-10
	motifs = []
	background_freq_log = np.log10(background_freq)
	with open(filename, 'r') as i:
		for line in i:
			line = line.strip()
			if len(line) > 0 and line[0] == '>':
				if counter == 0:
					try:
						motif = np.array(motif) + pseudocount
						# print(motif.sum(axis = 0))
						motif = np.log10(motif / motif.sum(axis = 0)) - background_freq_log
						motifs.append(motif)
					except UnboundLocalError:
						pass
					motif = [ [] for e in range(len(alphabet_order.keys())) ]
					counter += 1
				else:
					print("The format is wrong at " + line, file=sys.stderr)
					sys.exit()
			else:
				if line == '':
					counter = 0
					continue
				else:
					line = re.sub('[\[\]]', '', line)
					line = line.split()
					char = line.pop(0)
					char_num = [ float(num) for num in line ]
					motif[alphabet_order[char]] = char_num
					counter += 1
	motif = np.array(motif) + pseudocount
	motif = np.log10(motif / motif.sum(axis = 0)) - background_freq_log
	motifs.append(motif)
	return motifs

def get_background_freq(data):
	freq = [ float(i) for i in data.split(',') ]
	return np.array([freq]).T

def save_data(x, y, filename):
	f = h5py.File(filename, 'w')
	f.create_dataset('trainxdata', data=x)
	f.create_dataset('traindata', data=y)
	f.close()

def load_data(filename):
	f = h5py.File(filename, 'r')
	x = f['trainxdata'][()]
	y = f['traindata'][()]
	f.close()
	return (x, y)

class ModelAPI:
	def __init__(self, xshape, motifs):
		inputx = Input(shape=xshape)
		branches = []
		counter = 0
		nmotifs = len(motifs)
		for im in range(nmotifs):
			m = motifs[im]
			counter += 1
			# print(counter)
			motif_conv = Conv1D(filters=1,
					 kernel_size=m.transpose((1,0)).shape[0],
					 padding="valid",
					 strides=1,
					 activation='relu')(inputx)
			motif_max = MaxPooling1D(pool_size=xshape[0] - m.shape[1] + 1)(motif_conv)
			branches.append(motif_max)

		cat_conv = concatenate(branches, axis=-1)
		cat_conv = Flatten()(cat_conv)
		model = Model(inputs=inputx, outputs=cat_conv)
		self.xshape = xshape
		self.model = model
		self.weights = motifs
		self.nmotifs = nmotifs
	def assign_weight(self, threshold):
		layer_num = 1
		for im in range(self.nmotifs):
			m = self.weights[im]
			size_temp = list(m.transpose((1,0))[::-1].shape)
			size_temp.append(1)
			temp = np.zeros(size_temp)
			temp[:,:,0] = m.transpose((1,0))[::-1]
			self.model.layers[layer_num].set_weights([temp, np.array([-threshold])])
			layer_num += 1

class ModelCNN:
	def __init__(self, xshape, motifs):

		# determine the size of the biggest motif
		lmotif = 0
		for i in motifs:
			lmotif = max(lmotif, i.shape[1])

		# adding zeros to all motifs to make them at the same length
		new_motifs_left = []
		new_motifs_right = []
		for i in motifs:
			empty_left = np.zeros((4, lmotif))
			empty_right = np.zeros((4, lmotif))
			empty_left[:, :i.shape[1]] = i
			empty_right[:, -i.shape[1]:] = i
			new_motifs_left.append(empty_left)
			new_motifs_right.append(empty_right)
		new_motifs = new_motifs_left + new_motifs_right
		# build a sequential model
		model = Sequential()
		model.add(Conv1D(input_shape=xshape, filters=len(new_motifs),
								 kernel_size=lmotif,
								 padding="valid",
								 strides=1,
								 activation='relu'))
		model.add(MaxPooling1D(pool_size=xshape[0] - lmotif + 1))
		model.add(Reshape((2, int(len(new_motifs)  / 2))))
		model.add(MaxPooling1D(pool_size=2))
		model.add(Flatten())
		self.xshape = xshape
		self.model = model
		self.weights = new_motifs
		self.nmotifs = len(new_motifs)
	def assign_weight(self, threshold):
		motif_weights = np.zeros((self.weights[0].shape[1], self.weights[0].shape[0], self.nmotifs))
		for i in range(self.nmotifs):
			motif_weights[:,:,i] = self.weights[i].transpose((1,0))[::-1]
		self.model.layers[0].set_weights([motif_weights, np.ones((self.nmotifs,)) * -threshold])

def logistic_head(input_dim, output_dim, l1, l2):
	print('logistic head -- Building the model (l1 = {l1}, l2 = {l2})'.format(l1=l1, l2=l2))
	model = Sequential()
	model.add(Dense(output_dim, input_shape=(input_dim,), kernel_regularizer=regularizers.l1_l2(l1=l1, l2=l2)))
	model.add(Activation('sigmoid'))
	print('logistic head -- Compiling the model')
	model.compile(loss='binary_crossentropy', optimizer=SGD(), metrics=['accuracy'])
	return model
def svm_head(input_dim, output_dim, l2):
	print('svm head -- Building the model (lambda = {l2})'.format(l2=l2))
	model = Sequential()
	model.add(Dense(output_dim, input_shape=(input_dim,), kernel_regularizer=regularizers.l2(l2)))
	model.add(Activation('linear'))
	print('svm head -- Compiling the model')
	model.compile(loss='hinge', optimizer=SGD(), metrics=['accuracy'])
	return model
