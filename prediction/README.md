# Guideline of this module

## Config file

```
model: 'some/path.hdf5'  # Path to your location which can be loaded in keras
data:
  data-1: 'some/path'  # hdf5 and entry 'trainxdata' will be used
  data-2: 'some/path'
  data-3: 'some/path'
partition: 'gpu2'
prefix: 'TaskName'
```

Here `TaskName` should be model specific and the 'prediction' module is to make the prediction on various data sets using this model.

**Best practice**: Name config file as `config.TaskName.yaml`

## Generate `sbatch` file for prediction

```
$ snakemake --configfile config.TaskName.yaml
```

It will generate all `sbatch` scripts ready for submission.
