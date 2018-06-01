import argparse
parser = argparse.ArgumentParser(prog='merge.py', description='''
    Taking binarized positive and negative files (in HDF5) and output merged HDF5 with label
''')
parser.add_argument('--out')
parser.add_argument('--pos')
parser.add_argument('--neg')
args = parser.parse_args()

def mySubprocess(cmd, debug):
	if debug is False:
	    result = subprocess.check_output(cmd, shell=True)
	    return result
	else:
	    print(cmd)


import numpy as np
import h5py

pos = h5py.File(args.pos, 'r')
neg = h5py.File(args.neg, 'r')

meg = h5py.File(args.out, 'w')
npos = pos['trainxdata'].shape[0]
nneg = neg['trainxdata'].shape[0]
y = np.zeros(npos + nneg)
y[:npos] = 1
meg.create_dataset('trainxdata', data=np.concatenate((pos['trainxdata'][...], neg['trainxdata'][...]), axis = 0))
meg.create_dataset('traindata', data=y)
meg.close()
pos.close()
neg.close()
