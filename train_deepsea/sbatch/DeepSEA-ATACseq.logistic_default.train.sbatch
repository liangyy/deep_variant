#!/bin/bash
#SBATCH --job-name=DeepSEA-ATACseq.logistic_default
#SBATCH --output=DeepSEA-ATACseq.logistic_default.out
#SBATCH --error=DeepSEA-ATACseq.logistic_default.err
#SBATCH --time=24:00:00
#SBATCH --partition=gpu2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=50G
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
cd /project2/xinhe/yanyul
source setup.sh
source activate deepvarpred_test
module load cuda/7.5
cd repo/deep_variant/train_deepsea
mkdir train/DeepSEA-ATACseq.logistic_default/
python scripts/train_head_on_cluster.py --train /project2/xinhe/yanyul/deep_variant/yanyu/deep_brain/test/0629_ATACseq_merged/DeepSEA_train_12__with_label_with_label.hdf5 --valid /project2/xinhe/yanyul/deep_variant/yanyu/deep_brain/test/0629_ATACseq_merged/DeepSEA_valid_12__with_label_with_label.hdf5 --outdir train/DeepSEA-ATACseq.logistic_default/ --batch_size 100 --epoch 80 --l1 0 --l2 0 --head logistic
