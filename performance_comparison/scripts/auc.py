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

data = feather.read_dataframe(args.curve)
labels = pd.unique(data['data'])
sequences = pd.unqiue(data['info'])
curves = [ 'ROC', 'PR' ]
xy = { 'ROC': {'x': 'fpr', 'y': 'tpr'},
        'PR': {'x': 'recall', 'y': 'precision'} }

labels_out = []
sequence_out = []
curve_out = []
score_out = []

for label in labels:
    data_label = data[data['data'] == label]
    for sequence in sequences:
        data_sequence = data_label[data_label['info'] == sequence]
        for curve in curves:
            data_curve = data_sequence[data_sequence['type'] == curve]
            score = metrics.auc(data_curve[xy[curve]['x']], data_curve[xy[curve]['y']])
            labels_out.append(label)
            sequence_out.append(sequence)
            curve_out.append(curve)
            score_out.append(score)
table = pd.DataFrame({ 'data' : data_out, 'info' : sequence_out, 'curve' : curve_out, 'score': score_out})
feather.write_dataframe(table, args.out)
