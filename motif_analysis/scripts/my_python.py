from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from ntpath import basename
import os
os.environ['THEANO_FLAGS'] = "device=gpu"
os.environ['floatX'] = 'float32'
import subprocess
import h5py
import numpy as np
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
def reportHistogram(bins=None, counts=None):
	for i in range(len(counts)):
		start = bins[i]
		end = bins[i + 1]
		print('range {:.2f} - {:.2f} : {}'.format(start, end, counts[i]))
def saveData(hdf5file, name, data):
    f = h5py.File(hdf5file, 'w')
    f.create_dataset(name, data=data)
    f.close()
def getGradient_model(model, layer_idx, label_idx):
    # ATTENTION
    # layer_idx and label_idx should be 0-based
    from keras.models import load_model
    from keras.layers import Dense, Activation
    model = load_model(model)
    noutput = model.layers[-1].output_shape[1]
    model.add(Dense(1, name='extra_dense'))
    model.add(Activation('sigmoid', name='extra_activation'))
    import numpy as np
    linear = np.zeros((noutput, 1))
    linear[label_idx, 0] = 1
    bias = np.zeros((1))
    model.layers[-2].set_weights([linear, bias])
    model.compile(optimizer='sgd', loss='binary_crossentropy')
    gradients = model.optimizer.get_gradients(model.model.total_loss, [model.layers[layer_idx].output])
    import keras.backend as K
    input_tensors = [model.inputs[0], # input data
                     model.model.sample_weights[0], # how much to weight each sample by
                     model.model.targets[0], # labels
                     K.learning_phase(), # train or test mode
    ]
    get_gradients = K.function(inputs=input_tensors, outputs=gradients)
    return get_gradients

def getGradient_eval(get_gradients, sample):
    inputs = [[sample[0]], # X
          [1], # sample weights
          [sample[1]], # y
          0 # learning phase in TEST mode
    ]
    return get_gradients(inputs)[0]

def numSeqPerSeq(xlength, mask_size):
    return xlength - mask_size + 1 + 1 # add extra one  for original sequence

def newIdxByGroup(group_idx, ingroup_idx, group_size): # zero-base
    return group_idx * group_size + ingroup_idx

def log2Odds(matrix):
    return np.log2(matrix + 1e-10) - np.log2(1 - matrix + 1e-10)

def selectReadY(filename, name, label_idx, double, remove):
    y = getData(filename, name)
    if y.ndim == 2:
        y = y[:, label_idx - 1]
    if double == 'No':
    	y = np.hstack((y, y))
    if remove != 'None':
        temp = args.yremove.split('-')
        start = int(temp[0]) - 1
        end = int(temp[1])
    	if y.shape[0] % 2 == 1:
            my_python.eprint('y dim is not mod 2 zero. Cannot use double mode. Exit')
            sys.exit()
    	ny = int(y.shape[0] / 2)
        y = np.hstack((y[0:start], y[end:ny], y[ny:ny+start], y[ny+end:ny*2]))
    return y
