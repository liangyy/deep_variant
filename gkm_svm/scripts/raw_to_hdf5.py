import argparse
parser = argparse.ArgumentParser(prog='raw_to_hdf5.py', description='''
    Given gkm-SVM output, convert it into hdf5 format with true label
    (as the output of ../prediction)
''')
parser.add_argument('--predict')
parser.add_argument('--out')
args = parser.parse_args()

import h5py
import numpy as np
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python

ypred = np.loadtxt(args.predict, delimiter=',')
if y.shape[-1] != ypred.shape[-1]:
    print('The shape of y and y_pred do not match. Exiting', file=sys.stderr)
    sys.exit()
my_python.save_with_name(ypred, args.out, 'y_pred')
