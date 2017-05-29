import argparse
parser = argparse.ArgumentParser(prog='auc.py', description='''
    Given output curve file from pr_roc_curve module, compute the
    AUC of each curve
        ''')
parser.add_argument('--curve')
parser.add_argument('--out')
args = parser.parse_args()

from sklearn import metrics
import pandas as pd
import feather
import numpy as np

data = feather.read_dataframe(args.curve)
labels = pd.unique(data['data'])
sequences = pd.unique(data['info'])
curves = [ 'roc', 'pr' ]
xy = { 'roc': {'x': 'fpr', 'y': 'tpr'},
        'pr': {'x': 'recall', 'y': 'precision'} }

labels_out = []
sequence_out = []
curve_out = []
score_out = []

for label in labels:
    data_label = data[data['data'] == label]
    for sequence in sequences:
        data_sequence = data_label[data_label['info'] == sequence]
        for curve in curves:
            print('{label} - {sequence} - {curve}'.format(label=label, sequence=sequence, curve=curve))
            data_curve = data_sequence[data_sequence['type'] == curve]
            x = np.round(data_curve[xy[curve]['x']], decimals=10)
            y = np.round(data_curve[xy[curve]['y']], decimals=10)
            score = metrics.auc(x, y)
            labels_out.append(label)
            sequence_out.append(sequence)
            curve_out.append(curve)
            score_out.append(score)
table = pd.DataFrame({ 'data' : labels_out, 'info' : sequence_out, 'curve' : curve_out, 'score': score_out})
feather.write_dataframe(table, args.out)
