import argparse
parser = argparse.ArgumentParser(prog='assemble.py', description='''
    Given a file containing motifs info and the sequences we are working on,
    assemble a classifier that uses the indicator of if the sequence contains
    certain motif as features to predict outcome by logistic regression.

    Output input -> feature model and generate data for training and validation
    in standard format
        ''')
parser.add_argument('--motif', help='''
    Motif file in JASPAR format
''')
parser.add_argument('--background', help='''
    Background frequency (A,G,C,T)
''')
parser.add_argument('--xtrain', help='''
    Sequence file for training
''')
parser.add_argument('--xvalid', help='''
    Sequence file for validation
''')
parser.add_argument('--threshold', type=float, help='''
    Log likelihood ratio threshold to determine if the motif locates in sequence
''')
parser.add_argument('--output', help='''
    Save model in Keras format
''')
parser.add_argument('--output_train', help='''
    Save training data with feature representation in hdf5
''')
parser.add_argument('--output_valid', help='''
    Save validation data with feature representation in hdf5
''')
parser.add_argument('--ytrain', help='''
    Label file for training
''')
parser.add_argument('--yvalid', help='''
    Sequence file for validation
''')
args = parser.parse_args()

import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import numpy as np
import re
import h5py

import os
os.environ['THEANO_FLAGS'] = "device=gpu"
os.environ['floatX'] = 'float32'
from keras.models import Model, Sequential
from keras.layers import Conv1D, MaxPooling1D, Input, Flatten, Reshape
from keras.layers.merge import concatenate

sys.setrecursionlimit(10000)
alphabet_order = {  'A':0,
                    'G':1,
                    'C':2,
                    'T':3  }

xvalid = my_python.getData(args.xvalid, 'trainxdata')
xshape = xvalid.shape[1:]

background_freq = my_python.get_background_freq(args.background)

print('Reading Motif')
motifs = my_python.read_motif_from_jaspar(args.motif, background_freq, alphabet_order)

print('Building Model')
model = my_python.ModelCNN(xshape, motifs)

print('Compiling Model')
model.model.compile(loss='binary_crossentropy', optimizer='sgd')

print('Assigning Weights')
model.assign_weight(args.threshold)

print('Saving Model')
model.model.save(args.output)

print('Predicting on Validation Set')
feature_valid = model.model.predict(xvalid, verbose=1)
yvalid = my_python.getData(args.yvalid, 'traindata')
my_python.save_data(feature_valid, yvalid, args.output_valid)

print('Predicting on Training Set')
xtrain = my_python.getData(args.xtrain, 'trainxdata')
feature_train = model.model.predict(xtrain, verbose=1)
ytrain = my_python.getData(args.ytrain, 'traindata')
my_python.save_data(feature_train, ytrain, args.output_train)
