import argparse
parser = argparse.ArgumentParser(prog='sliding_window_compute.py', description='''
	Given sequences and model and output the prediction for each sequence (processed)
    by sliding_window_prepare)
	''')
parser.add_argument('--model')
parser.add_argument('--input')
parser.add_argument('--output')
parser.add_argument('--mask_size', type=int)
args = parser.parse_args()

from keras.models import load_model
import numpy as np
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import feather
import pandas as pd
import h5py

x_new = h5py.File(args.input, 'r')
name = list(x_new.keys())[0].decode()
xlength = int(name.split('-')[1])

model = load_model(args.model)
y_pred = model.predict(x, verbose=1)

num_of_seq_per_seq = my_python.numSeqPerSeq(x_new.shape[1], args.mask_size)
y_pred = y_pred.reshape((num_of_seq_per_seq, -1)).T
y_slide = y_pred[:num_of_seq_per_seq - 1]
y_origin = y_pred[num_of_seq_per_seq - 1]
y_slide = my_python.log2Odds(y_slide)
y_origin = my_python.log2Odds(y_origin)
y_delta = y_slide - y_origin
y_delta = y_delta.T
total_table = pd.DataFrame(y_delta, columns=[ 'Pos.' + str(i) for i in range(y_delta.shape[1]) ])
total_table = total_table.copy()
feather.write_dataframe(total_table, args.output)
