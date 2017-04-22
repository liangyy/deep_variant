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
# direction = (args.true_label - 0.5) * 2
direction = 1
moded_grad = my_python.getGradient_model(args.model, args.idx, args.label_idx - 1)
for i in range(x.shape[0]):
	print(i)
	seq = x[i, :, :]
	grad = my_python.getGradient_eval(moded_grad, [seq, np.ones((1)) * args.true_label])
	grad1 = np.max(grad, axis=1) # increase direction
	grad2 = np.min(grad, axis=1) # decrease direction
	grad = np.vstack((grad1, grad2))
	grad = np.hstack((grad, np.array([['max'], ['min']])))
	table = pd.DataFrame(grad)
	table_all = pd.concat([table_all, table])
table_all.columns = [ 'Motif.' + str(i) for i in range(grad.shape[1]) ] + [ 'Direction' ]
table_all = table_all.copy()
feather.write_dataframe(table_all, args.output)
