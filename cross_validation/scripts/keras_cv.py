# some idea is obtained from https://github.com/keras-team/keras/issues/1711

import argparse
parser = argparse.ArgumentParser(prog='cv.py', description='''
    Given the precomputed features from a feature representation model and true labels, perform [fold]-fold cross-validation on the input data sets. Output the predicted score of y and true y for each validation round
''')
parser.add_argument('--y', help='''
    HDF5 with true label in 'traindata'
''')
parser.add_argument('--x', help='''
    HDF5 with sequence in 'trainxdata'
''')
parser.add_argument('--classifier_type', help='''
    Type of classifier, 'logistic' or 'svm'
''')
parser.add_argument('--classifier_param', help='''
    Parameters of classifier, for example ('l1_l2'):
        'logistic': '3e-1_4e-2'
        'svm': '0_0.2' # l1 will not be used in svm!
''')
parser.add_argument('--fold', type=int, help='''
    The fold of CV
''')
parser.add_argument('--prefix', help='''
    Prefix of models built during CV and output TXT.GZ file containing the predicted score and true scores for each round
''')
args = parser.parse_args()

import sys
import importlib.util
spec = importlib.util.spec_from_file_location("my_python", "../baseline_classifier/scripts/my_python.py")
my_python = importlib.util.module_from_spec(spec)
spec.loader.exec_module(my_python)
import os
os.environ['THEANO_FLAGS'] = "device=gpu"
os.environ['floatX'] = 'float32'
import keras
from keras.callbacks import ModelCheckpoint, EarlyStopping

import numpy as np
import pandas as pd
import h5py
from sklearn.cross_validation import StratifiedKFold


def create_model(x_size, y_size, ctype, param):
    (l1, l2) = param.split('_')
    l1 = float(l1)
    l2 = float(l2)
    if ctype == 'logistic':
        model = my_python.logistic_head(x_size, y_size, l1, l2)
    elif ctype == 'svm':
        model = my_python.svm_head(x_size, y_size, l2)
    return model

def train_model(model, xtrain, ytrain, prefix):
    earlystopper = EarlyStopping(monitor='val_loss', patience=5, verbose=1)
    checkpointer = ModelCheckpoint(filepath=prefix + ".best.hdf5", monitor='val_loss', verbose=1, save_best_only=True, period=1)
    # Fit the model
    model.fit(xtrain, ytrain, validation_split=0.33, epochs=80, batch_size=10, shuffle=True, verbose=1, callbacks=[checkpointer, earlystopper])

def prediction(model, xtest, ytest, prefix):
    ypredict = model.predict(xtest)
    df = pd.DataFrame(data={'y_true': ytest, 'y_pred': ypredict[:, 0]})
    df.to_csv(prefix + 'predict.txt.gz', sep='\t', index=False, header=True, compression='gzip')

print('######## Loading data ########')
n_folds = args.fold
h1 = h5py.File(args.y, 'r')
label = h1['traindata'][...]
h1.close()
h2 = h5py.File(args.x, 'r')
feature = h2['trainxdata'][...]
h2.close()
print('finished!')
skf = StratifiedKFold(label, n_folds=n_folds, shuffle=True)

for i, (train, test) in enumerate(skf):
    print("######## Running Fold {n}/{k} ########".format(n=i+1, k=n_folds))
    model = None     
    print('1. Building and compiling model type = {type}, param = {param}'.format(type=args.classifier_type, param=args.classifier_param))
    model = create_model(feature.shape[-1], 1, args.classifier_type, args.classifier_param)
    print('2. Training model')
    train_model(model, feature[train], label[train], '{prefix}-{i}'.format(prefix=args.prefix, i=i+1))
    print('3. Predicting on test sequences')
    ypred = prediction(model, feature[test], label[test], '{prefix}-{i}'.format(prefix=args.prefix, i=i+1))
