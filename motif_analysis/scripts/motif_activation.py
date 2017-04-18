import argparse
parser = argparse.ArgumentParser(prog='motif_activation.py', description='''
	Given sequences and model and output the activation of convolutional layer
    (by layer index), where the spatial information is collapsed.
	''')
parser.add_argument('--model')
parser.add_argument('--input')
parser.add_argument('--output')
parser.add_argument('--idx', type=int)
args = parser.parse_args()

from keras.models import load_model
import numpy as np
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import feather
import pandas as pd

x = my_python.getData(args.input, 'x')

model = load_model(args.model)
from keras.models import Model
model_intermediate = Model(inputs=model.layers[0].input, outputs=model.layers[args.idx].output)
activation = model_intermediate.predict(x, verbose=1)
activation = np.max(activation, axis=1)
# my_python.saveData(args.output, 'y', activation)
total_table = pd.DataFrame(activation, columns=[ 'Motif.' + str(i) for i in range(activation.shape[1]) ])
total_table = total_table.copy()
feather.write_dataframe(total_table, args.output)
