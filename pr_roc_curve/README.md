# Guideline of this module

This module takes the

## Config file

In the report of this module, it plot ROC/PR curve for each group of curves (defined in config file) in a draw-down menu manor.

### Keep sequence set the same and compare different method

```
reweight: '1'  # Set it to '1' if you want to reweight every instance according to the GC content; set it to '0' otherwise
[TaskName]:
  group1:
    info: 'Method1'  # The name of the method
    data:
      [Label1]:
        y:
          path: 'some/path'  # In hdf5 format
          name: 'some name'  # Entry name
          label_idx: 1  # 1-based
          double: 'No'
          remove: 'None'
        ypred:
          path: 'some/path'  # The result of this method on predicting the labels of the specified sequence set (TaskName should specify sequence information)
          name: 'some name'
          label_idx: 1
          double: 'Yes'
          remove: 'None'
        gc: 'some/path'  # The result from gc_content module and match the sequence+label pair is REQUIRED
      [Label2]:
        y:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'No'
          remove: 'None'
        ypred:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'Yes'
          remove: 'None'
        gc: 'some/path'
  group2:
    info: 'Method2'
    data:
      [Label1]:  # It should match with the one in 'group1'
        y:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'No'
          remove: 'None'
        ypred:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'Yes'
          remove: 'None'
        gc: 'some/path'
      [Label2]:
        y:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'No'
          remove: 'None'
        ypred:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'Yes'
          remove: 'None'
        gc: 'some/path'
```

The item in draw-down list would be `LabelX` (every group should have the same set of `LabelX`; it may not be necessary but it is recommended; otherwise it is hard to say that it is making comparison). `MethodX` is to label each curve in the plot.

**Cautions**: You need to make sure that i) the predicted labels you provide in the config file match its asserted `MethodX` and `TaskName` (sequence+label); ii) `gc` matches sequence+label.

**Best practice**: Name the config file as `config.TaskName.yaml` where `TaskName` consists two pieces of information: i) sequence set; ii) if reweight, namely `TaskName` = `SequenceSet` or `SequenceSet.reweight`.

### Keep method the same and compare different sequence set

```
reweight: '1'  # Set it to '1' if you want to reweight every instance according to the GC content; set it to '0' otherwise
[TaskName]:
  group1:
    info: 'SequenceSet1'  # The name of the method
    data:
      [Label1]:
        y:
          path: 'some/path'  # In hdf5 format
          name: 'some name'  # Entry name
          label_idx: 1  # 1-based
          double: 'No'
          remove: 'None'
        ypred:
          path: 'some/path'  # The result of this method on predicting the labels of the specified sequence set (TaskName should specify sequence information)
          name: 'some name'
          label_idx: 1
          double: 'Yes'
          remove: 'None'
        gc: 'some/path'  # The result from gc_content module and match the sequence+label pair is REQUIRED
      [Label2]:
        y:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'No'
          remove: 'None'
        ypred:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'Yes'
          remove: 'None'
        gc: 'some/path'
  group2:
    info: 'SequenceSet1'
    data:
      [Label1]:  # It should match with the one in 'group1'
        y:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'No'
          remove: 'None'
        ypred:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'Yes'
          remove: 'None'
        gc: 'some/path'
      [Label2]:
        y:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'No'
          remove: 'None'
        ypred:
          path: 'some/path'
          name: 'some name'
          label_idx: 1
          double: 'Yes'
          remove: 'None'
        gc: 'some/path'
```

**Cautions**: You need to make sure that i) the predicted labels you provide in the config file match its asserted `SequenceSetX` and `TaskName` (method); ii) `gc` matches sequence+label.

**Best practice**: Name the config file as `config.TaskName.yaml` where `TaskName` consists two pieces of information: i) method; ii) if reweight, namely `TaskName` = `Method` or `Method.reweight`.

## Run the analysis

```
$ snakemake --configfile config.TaskName.yaml report/TaskName_plot.html
```
