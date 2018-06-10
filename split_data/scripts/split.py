import argparse
parser = argparse.ArgumentParser(prog='split.py', description='''
    Given training data, split it into two parts: training and validation sets. The fold controls the ratio of the size of these two sets. For instance, 5 fold means that the data is split into 5 parts and training takes 4 parts and validation takes one part
''')
parser.add_argument('--input', help='''
    HDF5 with true label in 'traindata'
''')
parser.add_argument('--fold', type=int, help='''
    The fold of CV
''')
parser.add_argument('--prefix', help='''
    Prefix of outputs (prefix.valid.hdf5 & prefix.train.hdf5)
''')
args = parser.parse_args()

import numpy as np
import h5py
from sklearn.cross_validation import StratifiedKFold

print('######## Loading data ########')
n_folds = args.fold
h1 = h5py.File(args.input, 'r')
label = h1['traindata'][...]
feature = h1['trainxdata'][...]
h1.close()
print('finished!')
skf = StratifiedKFold(label, n_folds=n_folds, shuffle=True)

for i, (train, test) in enumerate(skf):
    o = h5py.File('{prefix}.train.hdf5'.format(prefix = args.prefix), 'w')
    o.create_dataset('trainxdata', data = feature[train])
    o.create_dataset('traindata', data = label[train])
    o.close()
    o = h5py.File('{prefix}.valid.hdf5'.format(prefix = args.prefix), 'w')
    o.create_dataset('trainxdata', data = feature[test])
    o.create_dataset('traindata', data = label[test])
    o.close()
    break
