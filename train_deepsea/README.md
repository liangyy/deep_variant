# Guideline of this module

The whole logic is very similar to `baseline_classifier`.

## Config file

```
task_name: 'TaskName'
TaskName:
  niter: 80
  feature_model: 'some/path'  # It is the model that takes sequence (binary) as input and output the feature representation used for training the classification head (hdf5 format, keras)
  data:
    train: 'some/path' # In standard format (x: trainxdata, y: traindata)
    valid: 'some/path' # Same
Training:
  param-1:
    l1: a
    l2: b
partition: 'gpu2'
type_of_head: 'head-name'  # Either 'logistic' or 'svm'
selected_head:
  best: 'some/path'  # Specify this after training
```

For each training task, the specific information is training data (in our problem it contains two parts: i) sequence? (DeepSEA or experiment-specific); ii) label (which genomic annotation you are working with). Therefore TaskName should indicate this information.

**Best practice**: Name config file as `config.TaskName.head-name.yaml` or `config.TaskName.yaml`

## Training

### Generate `sbatch`

```
$ snakemake --configfile config.TaskName.yaml
```

### Select best model

Do this manually

## Merge head with body

Set the `selected_head` entry in config file.
```
selected_head:
  best: 'param-x/model-name'  # Add it by manually checking performance
```

Run:
```
$ snakemake model/TaskName_head-name.best.hdf5 --configfile config.TaskName.yaml
```
