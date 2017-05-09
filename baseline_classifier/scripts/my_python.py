import sys

from ntpath import basename
import os
import subprocess
import h5py
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
