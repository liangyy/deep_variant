import argparse
parser = argparse.ArgumentParser(prog='select_sequence.py', description='''
	Given the raw sequence x, true label y, and predicted label y_pred (all
    in HDF5 format), output the selected sequence for downstream motif analysis
	''')
parser.add_argument('--ypred', help='''
	y prediction in HDF5
	''')
parser.add_argument('--y', help='''
	y true label in HDF5
	''')
parser.add_argument('--x', help='''
	x raw sequence (binarized) in HDF5
	''')
parser.add_argument('--ypred_name', help='''
	dataset name in y predicted label HDF5
	''')
parser.add_argument('--y_name', help='''
	dataset name in y true label HDF5
	''')
parser.add_argument('--x_name', help='''
	dataset name in x HDF5
	''')
parser.add_argument('--num', type=int, help='''
	number of sequences you want to extract
	''')
parser.add_argument('--label_idx', type=int, help='''
	the label you would like to focus on
	''')
parser.add_argument('--out_pos', help='''
	positive sequences output filename
	''')
parser.add_argument('--out_neg', help='''
	negative sequences output filename
	''')
args = parser.parse_args()

import h5py
import numpy as np
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python, helper

y_pred = my_python.getData(args.ypred, args.ypred_name)
y_pred = y_pred[:, args.label_idx - 1]
y = my_python.getData(args.y, args.y_name)
y = y[:, args.label_idx - 1]
threhold_pos = helper.get_rough_threshold(y_pred[y == 1], args.num, 'max')
threhold_neg = helper.get_rough_threshold(y_pred[y == 0], args.num, 'min')
x = my_python.getData(args.x, args.x_name)
x_pos = x[y == 1][y_pred[y == 1] >= threhold_pos]
x_neg = x[y == 0][y_pred[y == 0] <= threhold_neg]
my_python.eprint('The threshold for positive instance is {tpos}'.format(tpos=threhold_pos))
my_python.eprint('The threshold for negative instance is {tneg}'.format(tneg=threhold_neg))
my_python.saveData(args.out_pos, 'x', x_pos)
my_python.saveData(args.out_neg, 'x', x_neg)
