import argparse
parser = argparse.ArgumentParser(prog='parse_file.py', description='''
    This script parses the file downloaded from http://hgdownload.cse.ucsc.edu/goldenPath/hg19/encodeDCC/wgEncodeUwDgf/files.txt
        ''')
parser.add_argument('--file')
parser.add_argument('--out')
args = parser.parse_args()

import re
import pandas as pd

title_dic = {'filename': []}
line = 0
with open(args.file, 'r') as f:
	for i in f:
		line += 1
		i = i.strip()
		info = i.split('\t')
		filename = info[0]
		title_dic['filename'].append(filename)
		info = info[1].split('; ')
		this_titles = []
		for sub in info:
			sub = sub.split('=')
			title = sub[0]
			content = sub[1]
			this_titles.append(title)
			if title in title_dic:
				title_dic[title].append(content)
			else:
				title_dic[title] = [ 'NA' for i in range(line - 1) ]
				title_dic[title].append(content)
		for t in title_dic.keys():
			if t not in this_titles:
				if t == 'filename':
					pass
				else:
					title_dic[t].append('NA')

table = pd.DataFrame(title_dic)
table.to_csv(args.out, sep=',')

