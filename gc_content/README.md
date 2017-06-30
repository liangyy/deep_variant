# Guideline of this module

## What to compute?

This module takes sequences and corresponding true labels and plot GC content distribution across positive sequences and negative ones. The predicted score is also required to make the comparison on the predictive power of GC content and the predicted score. But such comparison is not the main purpose of this module and it can be seen as a side-product. The main product is to get a sense on how the GC content as a covariate changes across positive instances and negative instances.

**Best practice**: It is recommended to do this analysis before using other evaluation module since if the 'reweight' mode (remove GC content bias contribution to predictive power) in those modules rely on the result generated here. However, it is recommended to do sequence-specific analysis only, namely avoid set up a group where the sequence sets overlap with other groups and the only difference is in predictive model.

## Config file

```
summary:
  Seq1-Labels: 'Seq1-1,Seq1-2,Seq1-3'
  Seq2-Labels: 'Seq2-1,Seq2-2,Seq2-3'
Seq1-1:
  data_ypred:
    path: 'some/path'  # In hdf5 format
    name: 'some name'  # Name of the entry
    double: 'Yes'  # If this variable contains the sequence information twice (for forward strand and backward strand respectively; order is all forwards + all backwards)
    remove: 'xxxx-xxxx'  # The interval of lines that should be removed (Consider forward lines only and backward ones will be taken care of accordingly; now we can only take one interval)
    label_num: 1  # the index (1-based) of column used
  data_y:
    label_num: -1  # If there is no need to specify the index of column, leave it as -1
    path: 'some/path'
    name: 'some name'
    double: 'No'
    remove: 'None'
  data_x:  # Note that this entry does NOT have 'remove'
    path: 'some/path'
    name: 'some name'
    double: 'Yes'
Seq1-2:
  ...
Seq1-3:
  ...
Seq2-1:
  ...
Seq2-2:
  ...
Seq2-3:
  ...
```

**Best practice**: Name the config file as `config.LabelSet.yaml`. Here LabelSet specify which genomic annotation you are working with. Note that the GC content bias depends on both sequence set and genomic annotation. Usually, SeqX-Labels should specify both sequence set and label information to avoid overwriting.

## Generate GC bias report

For each `SeqX-Labels` you specified inside `summary` in config file, do:

```
$ snakemake report/SeqX-Labels.gc_content.html --configfile config.LabelSet.yaml
```

It generate GC content report and also save the calculated GC content for the sequence+label pair for downstream analysis.
