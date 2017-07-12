import argparse
parser = argparse.ArgumentParser(prog='collect.py', description = '''
    Given the data in hdf5, collect `nseq` number of sequences from
    input sequence set. Output selected sequences in fasta format
    and the list of the indices of the selected sequences in txt
    format (separate by ',')
''')
parser.add_argument('--input', help='In hdf5 format with standard naming convention')
parser.add_argument('--nrepeat', type = int, help = 'Number of repeats')
parser.add_argument('--out_prefix')
parser.add_argument('--nseq', type = int, help = 'Number of repeats per selected subset')
args = parser.parse_args()

import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import numpy as np

x = my_python.read_standard_data_x(args.input)
for i in range(args.nrepeat):
    indice = np.random.choice(x.shape[0], args.nseq, replace = False)
    x_subset = np.take(x, indice, axis = 0)
    out_fasta = open('{prefix}_{i}.fa'.format(prefix = args.prefix, i = i), 'w')
    for j in range(len(indice)):
        idx = indice[j]
        seq = my_python.binary_to_char(x_subset[j])
        out_fasta.write('>{name}\n{seq}\n'.format(name))
    out_fasta.close()
    out_text = open('{prefix}_{i}.txt'.format(prefix = args.prefix, i = i), 'w')
    out_text.write(','.join([ str(idx) for idx in indice ]) + '\n')
    out_text.close()
