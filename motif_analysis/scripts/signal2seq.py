import argparse
parser = argparse.ArgumentParser(prog='signal2seq.py', description='''
    Take the output of sliding_window_signal2region.R, extract sequence
    accordingly (merge or not merge the selected overlaping sequences)
    and save as FASTA format (name with seq_id-start_pos-end_pos)

    The size of the extracted window should also be specified
''')
parser.add_argument('--position')
parser.add_argument('--sequence')
parser.add_argument('--mask_size', type=int)
parser.add_argument('--merge', type=int, help='''
    set --merge as 1 if want to merge ovelaps
''')
parser.add_argument('--window_size', type=int)
parser.add_argument('--out')
args = parser.parse_args()

import numpy as np
import h5py
import sys
if 'scripts/' not in sys.path:
    sys.path.insert(0, 'scripts/')
import my_python
import pandas as pd

alphabet_dic = { 0: 'A', 1: 'G', 2: 'C', 3: 'T'}
col_dic = { 'seq_id': 0, 'pos_id': 1 }
position = np.loadtxt(args.position, skiprows=1)
x_new = h5py.File(args.sequence, 'r')
name = list(x_new.keys())[0]
sequence = x_new[name][()]
x_new.close()

num_of_seq_per_seq = my_python.numSeqPerSeq(sequence.shape[1], args.mask_size)

seq_out = []
start_out = []
end_out = []
char_out = []
if args.merge == 1:
    start = position[0][col_dic['pos_id']] # 1-based
    end = position[0][col_dic['pos_id']] + args.mask_size # 1-based, not include
    seq_memory = position[0][col_dic['seq_id']]
    for i in range(1, position.shape[0] + 1):
        if i < position.shape[0]:
            seq = position[i][col_dic['seq_id']]
            pos = position[i][col_dic['pos_id']]
            if end - pos >= args.mask_size / 2 and seq == seq_memory:
                end = pos + args.mask_size
            else:
                if args.window_size:
                    if end - start + 1 > args.window_size:
                        pass
                    else:
                        delta = (args.window_size - (end - start)) / 2
                        start = max(1, start - delta)
                        end = min(end + delta, sequence.shape[1] + 1)
                seq_out.append(seq_memory)
                start_out.append(start)
                end_out.append(end)
                extracted = sequence[int(seq_memory * num_of_seq_per_seq - 1)][int(start - 1) : int(end - 1), :]
                ex_seq = ''
                for j in range(extracted.shape[0]):
                    num = extracted[j,:].argmax()
                    ex_seq = ex_seq + alphabet_dic[num]
                start = pos
                end = pos + args.mask_size
                seq_memory = seq
                char_out.append(ex_seq)
        else:
            if args.window_size:
                if end - start + 1 > args.window_size:
                    pass
                else:
                    delta = (args.window_size - (end - start)) / 2
                    start = max(1, start - delta)
                    end = min(end + delta, sequence.shape[1] + 1)
            seq_out.append(seq_memory)
            start_out.append(start)
            end_out.append(end)
            extracted = sequence[int(seq_memory * num_of_seq_per_seq - 1)][int(start - 1) : int(end - 1), :]
            ex_seq = ''
            for j in range(extracted.shape[0]):
                num = extracted[j,:].argmax()
                ex_seq = ex_seq + alphabet_dic[num]
            char_out.append(ex_seq)
elif args.merge != 1:
    for i in range(position.shape[0]):
        seq = position[i][col_dic['seq_id']]
        pos = position[i][col_dic['pos_id']]
        start = pos
        end = pos + args.mask_size
        if args.window_size:
            if end - start + 1 > args.window_size:
                pass
            else:
                delta = (args.window_size - (end - start)) / 2
                start = max(1, start - delta)
                end = min(end + delta, sequence.shape[1] + 1)
        extracted = sequence[int(seq_memory * num_of_seq_per_seq - 1)][int(start - 1) : int(end - 1), :]
        ex_seq = ''
        for j in range(extracted.shape[0]):
            num = extracted[j,:].argmax()
            ex_seq = ex_seq + alphabet_dic[num]
        seq_out.append(seq)
        start_out.append(start)
        end_out.append(end)
        char_out.append(ex_seq)
names = [ '-'.join([ str(int(j)) for j in i]) for i in zip(seq_out, start_out, end_out) ]
o = open(args.out, 'w')
for i in range(len(names)):
    o.write('>{name}\n'.format(name=names[i]))
    o.write(char_out[i] + '\n')
o.close()
# total_table = pd.DataFrame({ 'seq_id': seq_out, 'start_pos': start_out, 'end_pos': end_out, 'sequence': char_out})
# total_table.to_csv(args.out, compression='gzip', sep='\t', index=False)
