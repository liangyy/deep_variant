from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from ntpath import basename
import os
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
def saveData(hdf5file, name, data):
    f = h5py.File(hdf5file, 'w')
    f.create_dataset(name, data=data)
    f.close()

def computeGcWeights(y, gc, psuedocount=1):
    bins = [ float(i) / 20 for i in range(0, 21) ]
    pos_gc = gc[np.where(y == 1)]
    neg_gc = gc[np.where(y == 0)]
    pos_gc_count = np.histogram(pos_gc, bins=bins) + psuedocount
    neg_gc_count = np.histogram(neg_gc, bins=bins) + psuedocount
    bin_weights = pos_gc_count / neg_gc_count
    neg_idx = np.digitize(neg_gc, bins)
    weights = np.ones((y.shape[0]))
    for i in range(0, 21):
        weights[np.where(y == 0)][np.where(neg_idx == i + 1)] = bin_weights[i]
    return weights
