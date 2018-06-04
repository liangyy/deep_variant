#!/bin/bash
#SBATCH --job-name=cv.fantom-fetalbrain
#SBATCH --output=cv.fantom-fetalbrain.out
#SBATCH --error=cv.fantom-fetalbrain.err
#SBATCH --partition=gpu2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=50G
#SBATCH --nodes=1
#SBATCH --gres=gpu:1

cd /project2/xinhe/yanyul
source setup.sh
source activate deepvarpred_test
module load cuda/7.5 # load cuda dependency for theano to run on GPU. Now we use the default cuda library on RCC (v4.0)
cd /scratch/midway2/xinhe/repo/deep_variant/cross_validation
snakemake --configfile config.fantom-fetalbrain.yaml --unlock
snakemake --configfile config.fantom-fetalbrain.yaml --rerun-incomplete
