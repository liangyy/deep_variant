# Guideline of this module

## Config file

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
    x: 'hdf5 file with entry name trainxdata'
    y: 'hdf5 file with entry name traindata'  # it is not necessary during training but it is used to select best model
size: 5000 # number of sequences in training set
repeat: n
seed: 2017
window_size: 300
thread: 4
cache: 6000
```

  **Best practice**:
    1. Name config file as `config.[task].yaml`
    2. Use '-' to as space in `[label-name-x]` instead of '_'

## Prepare `sbatch` file for training

```
$ snakemake sbatch/TrainData_label-name-1.1.sbatch --configfile config.[task].yaml
```

  It generates `sbatch/TrainData_label-name-1.x.sbatch` where `x = 1, ..., n` with `n` specified by `repeat: n` in config file. Inside this call, it does the following things:
    1. For each repeat, randomly select instances from the training data
    2. Generate fasta file for gkm-SVM from training data in hdf5 format
