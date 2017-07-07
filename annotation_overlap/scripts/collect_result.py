import argparse
parser = argparse.ArgumentParser(prog='collect_result.py', description='''
    Collect the output of bedtools jaccard
''')
parser.add_argument('--files', narg='+')
parser.add_argument('--out')
args = parser.parse_args()

import pandas as pd

info_collected = pd.DataFrame()
names_a = []
names_b = []


for i in args.files:
    info = pd.read_table(i, sep='\t', header=0)
    name = i.split('__')
    name_a = name[1]
    name_b = name[2]
    info_collected.append(info)
    names_a.append(name_a)
    names_b.append(name_b)

names = pd.DataFrame({'name_1': names_a, 'name_2': names_b})
merged_data = pd.concat([info_collected, names], axis=1)
merged_data.to_csv(args.out, index=False)
