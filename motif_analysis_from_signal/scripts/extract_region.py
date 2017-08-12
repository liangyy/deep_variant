import argparse
parser = argparse.ArgumentParser(prog='extract_region.py', description='''
    Given a region list, randomly select [nregion] number of regions as output
''')
parser.add_argument('--region')
parser.add_argument('--nregion', type=int)
parser.add_argument('--output')
args = parser.parse_args()

import pandas as pd
import numpy as np

f = pd.read_table(args.bed, sep = '\t',
                                header = 0)
ntotal = f.shape[0]
selected_idx = np.random.choice(ntotal, replace = False)
selected_rows = f.iloc[selected_idx]
selected_rows.to_csv(args.output, sep = '\t', index = False, header = False, compression = 'gzip')
