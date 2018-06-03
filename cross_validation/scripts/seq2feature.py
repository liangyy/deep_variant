import argparse
parser = argparse.ArgumentParser(prog='seq2feature.py', description='''
    Given a sequence file and a feature representation in KERAS model format (HDF5), output the computed sequence feature in HDF5
''')
parser.add_argument('--input', help='''
    Sequence in HDF5 format with X labelled as trainxdata and Y labelled as traindata
''')
parser.add_argument('--feature', help='''
    The feature representation in KERAS model format (HDF5)
''')
parser.add_argument('--out', help='''
    Name of the output file
''')
args = parser.parse_args()

import sys
import numpy as np
import h5py
from keras.models import load_model

import os
os.environ['THEANO_FLAGS'] = "device=gpu"
os.environ['floatX'] = 'float32'

print('Loading data')
data = h5py.File(args.input, 'r')
x = data['trainxdata'][...]
data.close()

print('Loading feature model')
feature_model = load_model(args.feature)

print('Computing feature representation of input sequences')
x_feature = feature_model.model.predict(x, verbose=1)

print('Saving output')
o = h5py.File(args.output, 'w')
o.create_dataset('trainxdata', data=x_feature)
