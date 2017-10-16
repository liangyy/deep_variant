# Guideline of this module

## Config file

```
task_name: '[TaskName]'
[TaskName]:
  motifs: 'motifs/pfm_vertebrates.txt'
  background: '0.27665749,0.22330697,0.22330697,0.27665749'
  niter: 80
  threshold: 2 # LLR (base = 2) threshold to tell whether the sequence contains the motif
  data:
    train:
      x: 'sequence in hdf5 (binary) - entry name should be trainxdata'
      y: 'label in hdf5 (binary) - entry name should be traindata' # in standard format
    valid:
      x: 'follow same format as the above'
      y: 'follow same format as the above'
Training:
  [TrainName]:
    l1: 0
    l2: 0
partition: 'gpu2'
type_of_head: '[HeadName]'  # Either logistic or svm
selected_head:
  best: 'fill in this part after training (select the best model)'
```

  `TaskName` is should be task specific. task contains three parts:
    1. training data (till now, we limit our training data to be DeepSEA sequence
    only);
    2. which motif database is used
    3. which classifier is used (namely svm or logistic))

  Here, you don't have to care about naming different classifier head differently.
But for sequence+motif pair, you need to specify it.

  **Best practice**: name the config file as `config.[TaskName].[HeadName].yaml`

## Prepare motif representation

  This step is to generate motif representation given motif and sequence. It is
time-consuming so it is recommended to run it on cluster. See an `sbatch` file
example below.

```
#!/bin/bash
#SBATCH --job-name=JASPAR-ATACseq.feature
#SBATCH --output=JASPAR-ATACseq.feature.out
#SBATCH --error=JASPAR-ATACseq.feature.err
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
cd repo/deep_variant/baseline_classifier
snakemake prototype/TaskName.init.hdf5 --configfile config.TaskName.yaml --unlock
snakemake prototype/TaskName.init.hdf5 --configfile config.TaskName.yaml --rerun-incomplete
```

  It generates `prototype/TaskName.init.hdf5` which can be shared by all tasks
that have the same sequence+motif.

## Training

### Generate `sbatch`

```
$ snakemake --configfile config.[TaskName].[classifier_head].yaml
```

### Select best model

Do this manually. The second number is validation loss.

## Merge head with body

Set the `selected_head` entry in config file.
```
selected_head:
  best: '[TrainName]/[ModelName]'  # Add it by manually checking performance
```

Run:
```
$ snakemake model/[TaskName]_[HeadName].best.hdf5 --configfile config.[TaskName].[HeadName].yaml
```
