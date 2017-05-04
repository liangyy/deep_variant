import argparse
parser = argparse.ArgumentParser(prog='feather2meme.py', description='''
	Given PWM in feather format, output the MEME format ready for motif
    analysis
	''')
parser.add_argument('--feather')
parser.add_argument('--output')

args = parser.parse_args()

import numpy as np
import feather
import pandas as pd

o = open(args.output, 'w')
m = feather.read_dataframe(args.feather)
width = m.shape[1]
m = m.T[[0, 2, 1, 3]] # reorder bases to A, C, G, T
headline = 'MOTIF {motif} {motif}'.format(motif = args.feather)
matheader = 'letter-probability matrix:'
mat = m.to_string(index = False, header = False)
o.write(headline + '\n')
o.write(matheader + '\n')
o.write(mat)
o.close()
