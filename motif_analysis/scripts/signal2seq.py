import argparse
parser = argparse.ArgumentParser(prog='signal2seq.py', description='''
	Take the output of sliding_window_signal2region.R, extract sequence
    accordingly (merge or not merge the selected overlaping sequences)
    and save as table (seq_id, start_pos, end_pos, sequence)
''')
parser.add_argument('--position')
parser.add_argument('--sequence')
parser.add_argument('--mask_size', type=int)
parser.add_argument('--merge', type=int, help='''
    set --merge as 1 if want to merge ovelaps
''')
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
        extracted = sequence[int(seq_memory * num_of_seq_per_seq - 1)][int(start - 1) : int(end - 1), :]
        ex_seq = ''
        for j in range(extracted.shape[0]):
            num = extracted[j,:].argmax()
            ex_seq = ex_seq + alphabet_dic[num]
        seq_out.append(seq)
        start_out.append(start)
        end_out.append(end)
        char_out.append(ex_seq)
total_table = pd.DataFrame({ 'seq_id': seq_out, 'start_pos': start_out, 'end_pos': end_out, 'sequence': char_out})
total_table.to_csv(args.out, compression='gzip', sep='\t', index=False)
