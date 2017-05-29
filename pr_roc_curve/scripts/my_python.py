from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from ntpath import basename
import os
import subprocess
import h5py
import numpy as np
import pandas as pd

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

def computeGcWeights(y, yp, gc, psuedocount=1): # rearrange y, yp
    bins = [ float(i) / 20 for i in range(0, 21) ]
    pos_gc = gc[np.where(y == 1)[0]].as_matrix()
    neg_gc = gc[np.where(y == 0)[0]].as_matrix()
    pos_gc_count = np.histogram(pos_gc, bins=bins)[0] + psuedocount
    neg_gc_count = np.histogram(neg_gc, bins=bins)[0] + psuedocount
    bin_weights = pos_gc_count / neg_gc_count
    neg_idx = np.digitize(neg_gc, bins)
    weights_neg = pd.DataFrame(np.ones((neg_idx.shape[0])))
    for i in range(0, 20):
        weights_neg[0][np.where(neg_idx == i + 1)[0]] = bin_weights[i]
    weights_neg = weights_neg.as_matrix().T[0]
    weights = np.ones(int(y.sum()))
    weights = np.concatenate([weights, weights_neg])
    y_new = np.ones(int(y.sum()))
    y_new = np.concatenate([y_new, np.zeros(weights_neg.shape[0])])
    yp_new = yp[y == 1]
    yp_new = np.concatenate([yp_new, yp[y == 0]])
    return weights, y_new, yp_new
