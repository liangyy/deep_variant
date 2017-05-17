import argparse
parser = argparse.ArgumentParser(prog='raw_to_feather.py', description='''
    Given gkm-SVM output, convert it into feather format with true label
''')
parser.add_argument('--predict')
parser.add_argument('--truth')
parser.add_argument('--label', type=int)
parser.add_argument('--out')
args = parser.parse_args()

import h5py
import numpy as np
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import feather
import pandas as pd

y = my_python.read_standard(args.truth, 'traindata')
y = y[:, args.label-1]
ypred = data = np.loadtxt(args.predict, delimiter=',')
if y.shape[-1] != ypred.shape[-1]:
    print('The shape of y and y_pred do not match. Exiting', file=sys.stderr)
    sys.exit()
table = pd.DataFrame({ 'y' : y, 'y.predict' : ypred})
feather.write_dataframe(table, args.out)
