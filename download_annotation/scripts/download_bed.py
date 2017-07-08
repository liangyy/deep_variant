import argparse
parser = argparse.ArgumentParser(prog='download_bed.py', description='''
	Given a bed list and the index of the bed file that is wanted to download,
    download the bed file as the name specified by --out
	''')
parser.add_argument('--bed_list', help='''
	a text bed list with every row telling the url of the bed file
	''')
parser.add_argument('--id', type=int, help='''
	1-based
	''')
parser.add_argument('--out')
args = parser.parse_args()

import os
import numpy as np

e = np.genfromtxt(args.bed_list, skip_header=True, dtype=str)
bed_url = e[args.id - 1]
cmd = 'wget -O {out} {url}'.format(out=args.out, url=bed_url)
os.system(cmd)
