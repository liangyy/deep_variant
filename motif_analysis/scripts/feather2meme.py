import argparse
parser = argparse.ArgumentParser(prog='feather2meme.py', description='''
	Given PWM in feather format, output the MEME format ready for motif
    analysis
	''')
parser.add_argument('--feathers', nargs = '+')
parser.add_argument('--output')

args = parser.parse_args()

import numpy as np
import feather
import pandas as pd

o = open(args.output, 'w')
o.write('MEME version 4\n\n')
o.write('ALPHABET= ACGT\n\n')
for motif in args.feathers:
	m = feather.read_dataframe(motif)
	width = m.shape[1]
	m = m.T[[0, 2, 1, 3]] # reorder bases to A, C, G, T
	headline = 'MOTIF {motif} {motif}'.format(motif = motif)
	matheader = 'letter-probability matrix: alength= 4'
	mat = m.to_string(index = False, header = False)
	o.write(headline + '\n')
	o.write(matheader + '\n')
	o.write(mat + '\n')
o.close()
