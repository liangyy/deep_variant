import argparse
parser = argparse.ArgumentParser(prog='combine.py', description='''
    Combine all roc, pr curves
	''')
parser.add_argument('--files', nargs='+')
parser.add_argument('--output')
args = parser.parse_args()

import feather
import pandas as pd
table = pd.DataFrame()

for i in args.files:
    df = feather.read_dataframe(i)
    table = pd.concat([table, df])
feather.write_dataframe(table, args.output)
