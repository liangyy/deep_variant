# some idea is obtained from https://github.com/keras-team/keras/issues/1711

import argparse
parser = argparse.ArgumentParser(prog='cv.py', description='''
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

from sklearn.cross_validation import StratifiedKFold

def load_data():
    # load your data using this function

def create model():
    # create your model using this function

def train_and_evaluate__model(model, data[train], labels[train], data[test], labels[test)):
    model.fit...
    # fit and evaluate here.


n_folds = 10
data, labels, header_info = load_data()
skf = StratifiedKFold(labels, n_folds=n_folds, shuffle=True)

for i, (train, test) in enumerate(skf):
        print "Running Fold", i+1, "/", n_folds
        model = None # Clearing the NN.
        model = create_model()
        train_and_evaluate_model(model, data[train], labels[train], data[test], labels[test))
