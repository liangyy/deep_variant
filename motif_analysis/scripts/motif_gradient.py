import argparse
parser = argparse.ArgumentParser(prog='motif_gradient.py', description='''

	''')
parser.add_argument('--model')
parser.add_argument('--input')
parser.add_argument('--output')
parser.add_argument('--idx', type=int)
parser.add_argument('--label_idx', type=int)
parser.add_argument('--true_label', type=int)
args = parser.parse_args()

import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import feather
import pandas as pd
import numpy as np

x = my_python.getData(args.input, 'x')

table_all = pd.DataFrame()
direction = (args.true_label - 0.5) * 2

for i in range(x.shape[0]):
	seq = x[i, :, :]
	grad = my_python.getGradient(args.model, arg.idx, [seq, args.true_label], args.label_idx)
	grad = np.max(grad * direction, axis=1) # direction is consistent with label
	table = pd.DataFrame(grad)
	table_all = pd.concat([table_all, table])
table_all.columns = [ 'Motif.' + str(i) for i in range(grad.shape[1]) ]
table_all = total_table.copy()
feather.write_dataframe(table_all, args.output)
