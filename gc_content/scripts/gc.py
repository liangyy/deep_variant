import argparse
parser = argparse.ArgumentParser(prog='gc.py', description='''
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
parser.add_argument('--doublex')
parser.add_argument('--doubley')
parser.add_argument('--doubleyp')
parser.add_argument('--removey', help='1-based: remove [start]-[end]')
parser.add_argument('--removeyp')

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
# x = x[:, :, :2]
if args.doublex == 'Yes':
    x = x[:int(x.shape[0] / 2)]
gc = np.sum(x[:,:,1:3], axis = (1,2)) / x.shape[1]

y = my_python.getData(args.y, args.name_y)
if y.ndim == 2:
    y = y[:, args.idx_y - 1]
if args.doubley == 'Yes':
    if y.shape[0] % 2 == 1:
        my_python.eprint('y dim is not mod 2 zero. Cannot use double mode. Exit')
        sys.exit()
    ny = int(y.shape[0] / 2)
    y = y[:ny]
if args.removey != 'None':
    temp = args.removey.split('-')
    start = int(temp[0]) - 1
    end = int(temp[1])
    y = np.hstack((y[:start], y[end:]))

yp = my_python.getData(args.yp, args.name_yp)
if yp.ndim == 2:
    yp = yp[:, args.idx_yp - 1]
if args.doubleyp == 'Yes':
    if yp.shape[0] % 2 == 1:
        my_python.eprint('y_pred dim is not mod 2 zero. Cannot use double mode. Exit')
        sys.exit()
    nyp = int(yp.shape[0] / 2)
    yp = (yp[:nyp] + yp[nyp:]) / 2
if args.removeyp != 'None':
    temp = args.removeyp.split('-')
    start = int(temp[0]) - 1
    end = int(temp[1])
    yp = np.hstack((yp[:start], yp[end:]))
if yp.shape[0] != y.shape[0]:
    my_python.eprint('The number of sampels in y and y_pred does not match. Exit')
    sys.exit()


table = pd.DataFrame({ 'GC.Content' : gc, 'y' : y, 'y.predict' : yp})
feather.write_dataframe(table, args.out)
