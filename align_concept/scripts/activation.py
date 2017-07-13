import argparse
parser = argparse.ArgumentParser(prog = 'activation.py', description = '''
    Given a set of sequences with the indices of the selected subset,
    compute the activation of neurons of given models at given layers
''')
parser.add_argument('--input', help = '''
    In hdf5 format with standard naming convention
''')
parser.add_argument('--index', help = '''
    Text file with ',' as delimiter and index is 0-based
''')
parser.add_argument('--model')
parser.add_argument('--output')
parser.add_argument('--layers', help = '''
    String with the format [layer1_index],[layer2_index],...
''')
parser.add_argument('--names', help = '''
    String with the format [layer1_name],[layer2_name],...
''')
parser.add_argument('--length_n_jump', help = '''
    Specify the length of the window and the distance between the
    starting point of two adjacent windows. Use the format [l-j1],
    [l-j2], ...
''')
args = parser.parse_args()

import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
from keras.models import load_model
import numpy as np
from keras.models import Model

layers = [ int(i.strip()) for i in args.layers.split(',') ]
layer_names = [ i.strip() for i in args.names.split(',') ]
win_sizes = []
jumps = []
for i in args.length_n_jump.split(','):
    temp = i.strip().split('-')
    win_sizes.append(int(temp[0]))
    jumps.append(int(temp[1]))

model = load_model(args.model)
x = my_python.read_standard_data_x(args.input)
indice = np.loadtxt(args.index, delimiter = ',', dtype = int)
x_subset = np.take(x, indice, axis = 0)

for l in range(len(layers)):
    model_intermediate = Model(inputs=model.layers[0].input, outputs=model.layers[layers[l]].output)
    activation = model_intermediate.predict(x_subset, verbose = 1)
    spatial_x = np.array([ win_sizes[l] / 2 + j * jumps[l] for j in range(activation.shape[1]) ])
    my_python.save_layer(activation, spatial_x, layer_names[l], args.output)
