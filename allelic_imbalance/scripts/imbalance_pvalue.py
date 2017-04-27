import argparse
parser = argparse.ArgumentParser(prog='imbalance_pvalue.py', description='''
    Given VarScan final output (after filtering), calculate the fisher exact test p-value
    where in balanced case, we set ref/alt ratio should be 50/50.
	''')
parser.add_argument('--infile')
parser.add_argument('--outfile')
args = parser.parse_args()

import pandas as pd
import scipy.stats as stats

def fisher(inp):
    x1 = inp.Reads1
    x2 = inp.Reads2
    xm = (x1 + x2) / 2
    oddsratio, pvalue = stats.fisher_exact([[x1, x2], [xm, xm]])
    return {'Odds.Ratio': oddsratio, 'P.Value': pvalue}

table = pd.read_csv(args.infile, delimiter = '\t', header = 0, compression = 'gzip')
table['FishersExact'] = table.apply(
    x1 =
    lambda r: scipy.stats.fisher_exact([[r.Read1, r.Read2], []]),
    axis=1)
new_table = table.apply(lambda s: pd.Series(fisher(s)), axis=1)
table = pd.concat([table, new_table], axis=1)
table.to_csv(args.outfile, sep='\t', compression='gzip')
