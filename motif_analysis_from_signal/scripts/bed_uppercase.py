import argparse
parser = argparse.ArgumentParser(prog='bed_uppercase.py', description='''
    Convert all sequences to uppercase
''')
parser.add_argument('--input')
parser.add_argument('--out')
args = parser.parse_args()

o = open(args.out, 'w')
with open(args.input, 'r') as f:
    for i in f:
        if i[0] == '>':
            o.write(i)
        else:
            o.write(i.upper())
o.close()
