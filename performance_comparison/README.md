# Guideline of this module

This module is built upon the result of `pr_roc_curve` module. It combines the result of multiple outputs of `pr_roc_curve` and compute the bar plot to compare the AUC scores across different model+label+method tuples.

## Config file

### Combine different sequence sets

Each `feather` file listed is the result of a particular sequence set. In other word, the 'info' column in the file is the information of which method is used.

```
[TaskName]:
  [file-1]: 'some/path/pr_roc_curve/result/[some-name-1]_curves.feather'  # The output of pr_roc_curve module
  [file-2]: 'some/path/pr_roc_curve/result/[some-name-2]_curves.feather'
by: 'sequence'  # If the difference between files is the sequence set used, then set it as 'sequence'
```

### Combine different methods

Each `feather` file listed is the result of a particular methods across different sequence sets. In other word, the 'info' column in the file is the information of which sequence set is used.

```
[TaskName]:
  [file-1]: 'some/path/pr_roc_curve/result/[some-name-1]_curves.feather'  # The output of pr_roc_curve module
  [file-2]: 'some/path/pr_roc_curve/result/[some-name-2]_curves.feather'
by: 'model'  # DIFFERENCE is here
```

### Combine different other things

It is also possible to combine files with the difference other than the ones listed above. For instance, we can compare the result of the same sequence+method with/without considering GC bias. Since the 'info' column is still telling the method information, 'by' should be set as 'sequence' in the config file.

```
[TaskName]:
  [file.no-rewight]: 'some/path/pr_roc_curve/result/[some-name-1]_curves.feather'  # The output of pr_roc_curve module
  [file.reweight]: 'some/path/pr_roc_curve/result/[some-name-2]_curves.feather'
by: 'sequence'  # DIFFERENCE is here
```

**Caution**: The final plot will group different labels and color each bar by method but ignore the information of 'sequence' or other information. So, one thing to keep in mind is that the list of input files should share something.

**Best practice**: TaskName can be set as question-specific in high level with detailed information on what is compared if applicable, like LabelSet or LabelSet-Sequence.Reweight. Config file can be named accordingly, say `config.TaskName.yaml` or shorthand of it.

## Run the module

```
$ snakemake report/TaskName.auc_comparison.html --configfile config.TaskName.yaml
```

It is recommended to run it at backend using `nohup`. It won't take so long.
