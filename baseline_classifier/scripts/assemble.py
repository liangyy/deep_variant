import argparse
parser = argparse.ArgumentParser(prog='assemble.py', description='''
    Given a file containing motifs info and the sequences we are working on,
    assemble a classifier that uses the indicator of if the sequence contains
    certain motif as features to predict outcome by logistic regression
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
args = parser.parse_args()

import sys
if '../gc_content/scripts/' not in sys.path:
    sys.path.insert(0, '../gc_content/scripts/')
import my_python
import numpy as np
import re
import h5py

from keras.models import Model
from keras.layers import Conv1D, MaxPooling1D, Input
from keras.layers.merge import concatenate

alphabet_order = {  'A':0,
                    'G':1,
                    'C':2,
                    'T':3  }

def read_motif_from_jaspar(filename, background_freq, alphabet_order):
    counter = 0
    zero = 1e-12
    motifs = []
    background_freq_log = np.log10(background_freq + zero)
    with open(filename, 'r') as i:
        for line in i:
            line = line.strip()
            if len(line) > 0 and line[0] == '>':
                if counter == 0:
                    try:
                        motif = np.array(motif)
                        # print(motif.sum(axis = 0))
                        motif = np.log10(zero + motif / motif.sum(axis = 0)) - background_freq_log
                        motifs.append(motif)
                    except UnboundLocalError:
                        pass
                    motif = [ [] for e in range(len(alphabet_order.keys())) ]
                    counter += 1
                else:
                    print("The format is wrong at " + line, file=sys.stderr)
                    sys.exit()
            else:
                if line == '':
                    counter = 0
                    continue
                else:
                    line = re.sub('[\[\]]', '', line)
                    line = line.split()
                    char = line.pop(0)
                    char_num = [ float(num) for num in line ]
                    motif[alphabet_order[char]] = char_num
                    counter += 1
    return motifs

def get_background_freq(data):
    freq = [ float(i) for i in data.split(',') ]
    return np.array([freq]).T

xvalid = my_python.getData(args.xvalid, 'trainxdata')
xshape = xvalid.shape[1:]

background_freq = get_background_freq(args.background)
motifs = read_motif_from_jaspar(args.motif, background_freq, alphabet_order)

inputx = Input(shape=xshape)
branches = []
counter = 0
for m in motifs:
    counter += 1
    print(counter)
    motif_conv = Conv1D(filters=1,
                             kernel_size=m.transpose((1,0)).shape[0],
                             padding="valid",
                             strides=1,
                             activation='relu')(inputx)
    motif_max = MaxPooling1D(pool_size=xshape[0] - m.shape[1] + 1)(motif_conv)
    branches.append(motif_max)


cat_conv = concatenate(branches, axis=-1)
model = Model(inputs=inputx, outputs=cat_conv)
model.compile(loss='binary_crossentropy', optimizer='sgd')
model.summary()
