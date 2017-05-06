import argparse
parser = argparse.ArgumentParser(prog='curve.py', description='''
    Given x, y, y_pred, output a feather file containing GC content,
    y, and y_pred per sequence
        ''')
parser.add_argument('--x')
parser.add_argument('--y')
parser.add_argument('--yp')
parser.add_argument('--name_x')
parser.add_argument('--name_y')
parser.add_argument('--name_yp')
parser.add_argument('--idx_y', type=int, help='1-based')
parser.add_argument('--idx_yp', type=int, help='1-based')
parser.add_argument('--out')
args = parser.parse_args()

from sklearn.metrics import precision_recall_curve
from sklearn import metrics
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import numpy as np
import pandas as pd
import feather

x = my_python.getData(args.x, args.name_x)
x = x[:, :, :2]
gc = np.sum(x[:,:,1:3], axis = (1,2)) / x.shape[1]
y = my_python.getData(args.y, args.name_y)
y = y[:, args.idx_y]
y_pred = my_python.getData(args.yp, args.name_yp)
y_pred = y_pred[:, args.idx_yp]

table = pd.DataFrame({ 'GC.Content' : gc, 'y' : y, 'y.predict' : y_pred})
feather.write_dataframe(table, args.out)
