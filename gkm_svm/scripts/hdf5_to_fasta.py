import argparse
parser = argparse.ArgumentParser(prog='hdf5_to_fasta.py', description='''
    Given split/not split hdf5 file and output fasta file correspondingly
''')
parser.add_argument('--split', type=int, help='''
    If the input data has been split (all positive or all negative), then
    use --split 1, otherwise use --split 0
''')
parser.add_argument('--window', type=int)
parser.add_argument('--data')
parser.add_argument('--out')
args = parser.parse_args()

import h5py
import numpy as np
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python

if args.split == 1:
    x = my_python.read_standard(args.data, 'trainxdata')
    my_python.binary_to_fasta(x, args.out, args.window)
elif args.split == 0:
    x = my_python.read_standard(args.data, 'trainxdata')
    y = my_python.read_standard(args.data, 'traindata')
    x, y = my_python.check_and_shrink(x, y)
    xpos = x[y == 1]
    xneg = x[y == 0]
    my_python.binary_to_fasta(xpos, args.out[0], args.window)
    my_python.binary_to_fasta(xneg, args.out[1], args.window)
