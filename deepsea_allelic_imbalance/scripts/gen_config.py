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
        filepath = args.url_prefix + os.sep + i
        i = ntpath.basename(i)
        i = '.'.join(i.split('.')[:-1])
        w = '''{name}: '{fileurl}'
'''.format(name=i, fileurl=filepath)
        o.write(w)
o.close()
