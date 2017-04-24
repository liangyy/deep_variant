import argparse
parser = argparse.ArgumentParser(prog='curve.py', description='''
    Given y and y_pred, output a feather file contains PR curve
	''')
parser.add_argument('--ypath')
parser.add_argument('--yname')
parser.add_argument('--yidx', type=int, help='1-based')
parser.add_argument('--yppath')
parser.add_argument('--ypname')
parser.add_argument('--ypidx', type=int, help='1-based')
parser.add_argument('--output')
parser.add_argument('--mode')
parser.add_argument('--name')
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

y = my_python.getData(args.ypath, args.yname)
y = y[:, args.yidx - 1]
ny = y.shape[0] / 2
y = y[:ny]

yp = my_python.getData(args.yppath, args.ypname)
yp = y[:, args.ypidx - 1]
nyp = yp.shape[0] / 2
if nyp != ny:
    my_python.eprint('The number of sampels in y and y_pred does not match. Exit')
    sys.exit()
yp = (yp[:nyp] + yp[nyp:]) / 2

if args.mode == 'pr':
    precision, recall, thresholds = precision_recall_curve(y, yp)
    thresholds = np.hstack((thresholds, 1))
    table = pd.DataFrame({ 'precision' : precision, 'recall' : recall, 'thresholds' : thresholds, 'data': args.name, 'type': args.mode})
elif args.mode == 'roc':
    fpr, tpr, thresholds = metrics.roc_curve(y, yp)
    table = pd.DataFrame({ 'fpr' : fpr, 'tpr' : tpr, 'thresholds' : thresholds, 'data': args.name, 'type': args.mode})
feather.write_dataframe(table, args.output)
