import argparse
parser = argparse.ArgumentParser(prog='hdf5motif2pwm.py', description='''
	Given test sequences and model with motif layer index, output the transformed
    PWM representation of motif by summarizing the sequences that can activate the
    the motif with more than the maximum activity
	''')
parser.add_argument('--model')
parser.add_argument('--data')
parser.add_argument('--layer_idx', type=int)
parser.add_argument('--nmotifs', type=int)
parser.add_argument('--data_name')
parser.add_argument('--output', nargs='+')
parser.add_argument('--lmotif', type=int)
args = parser.parse_args()

from keras.models import load_model
import numpy as np
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import feather
import pandas as pd

x = my_python.getData(args.data, args.data_name)

model = load_model(args.model)
from keras.models import Model
model_intermediate = Model(inputs=model.layers[0].input, outputs=model.layers[args.layer_idx].output)
activation = model_intermediate.predict(x, verbose=1)
amax_value = np.max(activation, axis=1)
amax_pos = np.argmax(activation, axis=1)
motif_pwm = np.zeros((args.lmotif, 4, args.nmotifs))
motif_cumweights = np.zeros((args.nmotifs))
for seq_i in range(amax_value.shape[0])
    for motif_j in range(amax_value.shape[1]):
        if amax_value[seq_i, motif_j] < 0:
            continue
        pos = amax_pos[seq_i, motif_j]
        subx = x[seq_i, pos : pos + args.lmotif]
        motif_pwm[:, :, motif_j] += amax_value[seq_i, motif_j] * subx
        motif_cumweights[motif_j] += amax_value[seq_i, motif_j]
for motif_j in range(amax_value.shape[1]):
    motif_pwm[:, :, motif_j] /= motif_cumweights[motif_j]
    total_table = pd.DataFrame(motif_pwm[motif_j].transpose((1,0)), columns=[ 'Pos.' + str(i) for i in range(args.lmotif) ])
    total_table = total_table.copy()
    feather.write_dataframe(total_table, output[motif_j])
