# Overview

This pipeline contains two main steps:
1. extract a subset of sequences of interest for downstream analysis
2. take the subset sequences and generate the patterns of interest

# Environment

```
$ source activate deepvar_motif
```

# Steps

To get a set of selected sequences for downstream analysis:
```
$ snakemake data/E081/selected_positive.hdf5
```

# TODO

1. implement `mutagensis` [link](modules/seq2pattern/_mutagensis.snakemake)
2. implement `sliding_window` [link](modules/seq2pattern/_sliding_window.snakemake)
3. implement `motif_gradient` [link](modules/seq2pattern/_motif_gradient.snakemake)
4. implement `motif_activation` [link](modules/seq2pattern/_motif_activation.snakemake)
