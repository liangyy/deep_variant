import argparse
parser = argparse.ArgumentParser(prog='hdf5_to_fasta.py', description='''
    Randomly generate subset of input sequences (positive, negative sets
    are balanced)
''')
parser.add_argument('--x')
parser.add_argument('--y')
parser.add_argument('--nsubset', type=int)
parser.add_argument('--prefix')
parser.add_argument('--seed', type=int)
parser.add_argument('--size', type=int)
parser.add_argument('--label', type=int)

args = parser.parse_args()

import h5py
import numpy as np
import sys

def read_standard(filename, name):
    f = h5py.File(filename, 'r')
    x = f[name][()]
    f.close()
    return x
def save_standard(data, filename):
    f = h5py.File(filename, 'w')
    f.create_dataset('trainxdata', data=data)
    f.close()

x = read_standard(args.x, 'trainxdata')
y = read_standard(args.y, 'traindata')
pos_idx = np.where(y[:, args.label-1] == 1)[0]
print(pos_idx[:10])
neg_idx = np.where(y[:, args.label-1] == 0)[0]
print(neg_idx[:10])
npos = pos_idx.shape[0]
nneg = neg_idx.shape[0]

if npos < args.size or nneg < args.size:
    print('The size set for output is too big. Exiting', file=sys.stderr)
    sys.exit()

ppos = float(args.size) / npos
pneg = float(args.size) / nneg

np.random.seed(args.seed)
for i in range(1, args.nsubset + 1):
    rpos = np.random.rand(npos) < ppos
    rneg = np.random.rand(nneg) < pneg
    print(pos_idx[rpos])
    print(neg_idx[rneg])
    subpos = x[pos_idx[rpos]]
    subneg = x[neg_idx[rneg]]
    save_standard(subpos, '{prefix}.{id}.pos.hdf5'.format(prefix=args.prefix, id=i))
    save_standard(subneg, '{prefix}.{id}.neg.hdf5'.format(prefix=args.prefix, id=i))
