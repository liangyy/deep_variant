import argparse
parser = argparse.ArgumentParser(prog='gen_pred_sbatch.py', description='''
    Generate the sbatch script for prediction task
    Specify the model and prediction data and configfile you want to use
    Output at sbatch with the same naming convention as Snakemake
''')
parser.add_argument('--model')
parser.add_argument('--data_tag', help='''
    Validation (prediction) data tag in config file
''')
# parser.add_argument('--desired_out', help='''
#     What you want as output of snakemake
#     I.e. result/deepsea_train_E081.1.deepsea_test.hdf5
# ''')
parser.add_argument('--config', help='''
    Name of config file for --configfile tag in snakemake call
''')
parser.add_argument('--wd', help='''
    working directory
''')
args = parser.parse_args()

import re
import os

model_info = re.sub('model/', '', args.model)
model_info = re.sub('.model.txt', '', model_info)
data_info = args.data_tag
desired_out = 'result/{model}.{data}.hdf5'.format(model=model_info, data=data_info)

sbatch = '''#!/bin/bash
#SBATCH --job-name={data}.{model}
#SBATCH --output={data}.{model}.out
#SBATCH --error={data}.{model}.err
#SBATCH --time=24:00:00
#SBATCH --partition=broadwl
#SBATCH --mem-per-cpu=50G
#SBATCH --nodes=1

cd /project2/xinhe/yanyul
source setup.sh
source activate deepvarpred_test
cd {wd}
snakemake --unlock {desired_out} --configfile {config}
snakemake --rerun-incomplete {desired_out} --configfile {config}
'''.format(data=data_info, model=model_info, desired_out=desired_out, config=args.config, wd=args.wd)

outname = 'sbatch/{data}.{model}.sbatch'.format(data=data_info, model=model_info)
o = open(outname, 'w')
o.write(sbatch)
o.close()

os.system('snakemake -np {desired_out} --configfile {config}'.format(desired_out=desired_out, config=args.config))
