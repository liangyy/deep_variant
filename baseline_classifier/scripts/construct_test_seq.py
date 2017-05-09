import argparse
parser = argparse.ArgumentParser(prog='construct_test_seq.py', description='''
    Given the sequences in character and the size of shift relative to the start,
    output hdf5 file that contains these sequences in standard format
''')
parser.add_argument('--seqs', nargs='+', help='''
    [seq,shift_size]
''')
parser.add_argument('--out')
args = parser.parse_args()

import h5py
import numpy as np

x = np.zeros((len(args.seqs), 1000, 4))
char_id = {'A':0, 'G':1, 'C':2, 'T':3}
for i in range(len(args.seqs)):
    seq = args.seqs[i]
    seq = seq.split(',')
    shift = int(seq[1])
    seq = list(seq[0])
    for j in range(len(seq)):
        x[i, j + shift, char_id[seq[j]]] = 1

f = h5py.File(args.out, 'w')
f.create_dataset('trainxdata', data=x)
f.close()
