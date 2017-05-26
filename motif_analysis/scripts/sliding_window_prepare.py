import argparse
parser = argparse.ArgumentParser(prog='sliding_window_prepare.py', description='''
	Given a set of sequences, generate the input file  ready for sliding window analysis,
    where for each sequence do mask the part of sequence by mask_size (set as zeros)
	''')
parser.add_argument('--input')
parser.add_argument('--mask_size', type=int)
parser.add_argument('--output')
args = parser.parse_args()

import h5py
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import numpy as np

x = my_python.getData(args.input, 'x')
num_of_seq_per_seq = my_python.numSeqPerSeq(x.shape[1], args.mask_size)
new_x = np.zeros((x.shape[0] * num_of_seq_per_seq, x.shape[1], x.shape[2]))
for i in range(x.shape[0]):
    for j in range(num_of_seq_per_seq - 1):
        index = my_python.newIdxByGroup(i, j, num_of_seq_per_seq)
        start = j
        end = j + args.mask_size
        end = min(end, x.shape[1])
        new_x[index] = x[i]
        new_x[index, start : end, :] = 0.25
    index = my_python.newIdxByGroup(i, num_of_seq_per_seq - 1, num_of_seq_per_seq)
    new_x[index] = x[i]
my_python.saveData(args.output, '-'.join(['x', str(x.shape[1])]), new_x)
