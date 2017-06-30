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

### Config for prediction

```
label:
  [label-name-1]: 1
  [label-name-2]: 2
  [label-name-3]: 3
  [label-name-4]: 4
training_data:
  [TrainData]:
    x: '' # Not used in prediction
    y: ''
validation_data:
  [PredictData]:
    x: 'hdf5 file with entry name trainxdata'
    y: 'None' # It is not needed
size: -1 # Per label, not used in prediction phase
repeat: 3
seed: 2017
window_size: 300
thread: 4
cache: 6000
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

## Make prediction on test data

Manually select model among all repeats for each label. Make use of the report generated in the previous step. Take ROC and PR curve into consideration together.

## Prepare `sbatch` script for prediction

Suppose the ith repeat is selected for label `label-name-x`. Generate the script as follow:

```
$ python scripts/gen_pred_sbatch.py --model model/[TrainData]_[label-name-x].i.model.txt --data_tag [PredictData] --config config_pred.[task].yaml
```
