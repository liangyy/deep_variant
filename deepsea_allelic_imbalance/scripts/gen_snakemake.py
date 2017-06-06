import argparse
parser = argparse.ArgumentParser(prog='gen_sbatch_yaml.py', description='''
    This script generates sbatch script given a config file
''')
parser.add_argument('--config')
args = parser.parse_args()

import ntpath
import os
import yaml

name = ntpath.basename(args.config)
name = '.'.join(name.split('.')[:-1])
con = yaml.load(open(args.config, 'r'))
for i in con.keys():
    if i in ['genome_assembly', 'model', 'call_varscan']:
        continue
    wanted = 'data/config.{name}.allelic_imbalance.yaml'.format(name=i)
    snmk = 'snakemake --configfile {config} {wanted}'.format(config=args.config, wanted=wanted)
    os.system(snmk + ' -np')
    sbatch = '''#!/bin/bash
#SBATCH --job-name={name}_yaml
#SBATCH --output={name}_yaml.out
#SBATCH --error={name}_yaml.err
#SBATCH --time=24:00:00
#SBATCH --partition=broadwl
#SBATCH --mem-per-cpu=50G
#SBATCH --nodes=1

cd /project2/xinhe/yanyul
source setup.sh
source activate deepvarpred_test
cd repo/deep_variant/deepsea_allelic_imbalance
{snmk} --unlock
{snmk} --rerun-incomplete
'''.format(name=i, snmk=snmk)
    o = open('sbatch/{name}.yaml.sbatch', name=i)
    o.write(sbatch)
    o.close()
