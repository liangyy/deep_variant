import argparse
parser = argparse.ArgumentParser(prog='filtering.py', description='''
    Given VarScan output, filter out rows that have too few allele1 count
	''')
parser.add_argument('--infile')
parser.add_argument('--outfile')
args = parser.parse_args()

import pandas as pd
table = pd.read_csv(args.infile, delimiter = '\t', header = 0, compression = 'gzip')
filtered_table = table[table['Reads1'] >= 20]
filtered_table.to_csv(args.outfile, sep='\t', compression='gzip')
