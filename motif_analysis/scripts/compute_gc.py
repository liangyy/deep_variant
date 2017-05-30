import argparse
parser = argparse.ArgumentParser(prog='compute_gc.py')
parser.add_argument('--pos')
parser.add_argument('--neg')
parser.add_argument('--out')
args = parser.parse_args()

import numpy as np
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import feather
import pandas as pd

x_pos = my_python.getData(args.pos, 'x')
gc_pos = np.sum(x_pos[:,:,1:3], axis = (1,2)) / x_pos.shape[1]
y_pos = np.ones(x_pos.shape[0])

x_neg = my_python.getData(args.neg, 'x')
gc_neg = np.sum(x_neg[:,:,1:3], axis = (1,2)) / x_neg.shape[1]
y_neg = np.zeros(x_neg.shape[0])

gc = np.hstack((gc_pos, gc_neg))
y = np.hstack((y_pos, y_neg))
table = pd.DataFrame({ 'GC.Content' : gc, 'y' : y})
feather.write_dataframe(table, args.out)
