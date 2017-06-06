import argparse
parser = argparse.ArgumentParser(prog='gen_config.py', description='''
    This script generates config file given a bam file list
''')
parser.add_argument('--file_list')
parser.add_argument('--url_prefix')
parser.add_argument('--out')
args = parser.parse_args()

import ntpath
import os

o = open(args.out, 'w')
with open(args.file_list, 'r') as f:
    for i in f:
        i = i.strip()
        i = i.split(' ')
        idx = i[1]
        i = i[0]
        filepath = args.url_prefix + os.sep + i
        i = ntpath.basename(i)
        i = '.'.join(i.split('.')[:-1])
        w = '''{name}:
    path: '{fileurl}'
    label_idx: {idx}
'''.format(name=i, fileurl=filepath, idx=idx)
        o.write(w)
o.close()
