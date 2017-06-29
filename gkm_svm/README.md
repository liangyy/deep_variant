# Guideline of this module

## Config file

### Config for training

```
label:
  [label-name-1]: 1
  [label-name-2]: 2
  [label-name-3]: 3
  [label-name-4]: 4
training_data:
  [TrainData]:
    x: 'hdf5 file with entry name trainxdata'
    y: 'hdf5 file with entry name traindata'
validation_data:
  [ValidData]:
    x: 'hdf5 file with entry name trainxdata' # it is not necessary during training but it is used to select best model. Use the validation set
    y: 'hdf5 file with entry name traindata'
size: 5000 # number of sequences in training set
repeat: n
seed: 2017
window_size: 300
thread: 4
cache: 6000
```

### Config for testing

```
```

  **Best practice**:
    1. Name config file as `config_train.[task].yaml` and `config_pred.[task].yaml` respectively
    2. Use '-' to as space in `[label-name-x]` instead of '_'

## Prepare `sbatch` file for training

```
$ snakemake sbatch/TrainData_label-name-1.1.sbatch --configfile config.[task].yaml
```

  It generates `sbatch/TrainData_label-name-1.x.sbatch` where `x = 1, ..., n` with `n` specified by `repeat: n` in config file. Inside this call, it does the following things:
    1. For each repeat, randomly select instances from the training data
    2. Generate fasta file for gkm-SVM from training data in hdf5 format

## Generate validation report

Test the performance on a validation data set.

```
$ snakemake report/deepsea_train-ATACseq.deepsea_valid-ATACseq.training_report.html --configfile config_train.atac.yaml
```

You can either run it on backend or on cluster (It may take long time).