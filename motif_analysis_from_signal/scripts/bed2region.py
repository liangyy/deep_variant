import argparse
parser = argparse.ArgumentParser(prog='bed2region.py', description='''
    Take a bed file and output a list of regions that are split from the regions
    in the bed file with the region length defined in window_size
''')
parser.add_argument('--bed')
parser.add_argument('--window_size')
parser.add_argument('--output')
args = parser.parse_args()

import pandas as pd

def split_to_region(group, *args):
    row = group.iloc[0]
    chrm = row['chr']
    start = int(row['start'])
    end = int(row['end'])
    if args[0] == 'free':
        nregion = 1
    else:
        window_size = int(args[0])
        nregion = end - start - window_size + 1
    chrm_new = [chrm] * nregion
    start_new = [ start + i for i in range(nregion) ]
    end_new = [ start + i + window_size for i in range(nregion) ]
    ret = pd.DataFrame({'chr': chrm_new, 'start': start_new, 'end': end_new})
    return ret


f = pd.read_table(args.bed, sep = '\t',
                                header = None,
                                names = ['chr', 'start', 'end'],
                                usecols = [0, 1, 2])
out = f.groupby(['chr', 'start', 'end'],
                    group_keys = False).apply(split_to_region, args.window_size)
out.to_csv(args.output, sep = '\t', index = False, compression = 'gzip')
