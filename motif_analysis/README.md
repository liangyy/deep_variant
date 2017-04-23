# Overview

This pipeline contains two main steps:
1. extract a subset of sequences of interest for downstream analysis
2. take the subset sequences and generate the patterns of interest

# Environment

```
$ source activate deepvar_motif
```
R dependencies: `bsselectR`

# Steps

To get a set of selected sequences for downstream analysis:
```
$ snakemake data/E081/selected_positive.hdf5
```

To generate the analysis of motif activation, run:
```
$ snakemake report/Type1/E081/motif_activation.html
```
See an example at `report/Type1/E081/motif_analysis.html`

# TODO

1. implement `mutagensis` [link](modules/seq2pattern/_mutagensis.snakemake)
2. implement `sliding_window` [link](modules/seq2pattern/_sliding_window.snakemake)
3. implement `motif_gradient` [link](modules/seq2pattern/_motif_gradient.snakemake)
    - implement a function that takes the model, single sample, label index, and the layer index and output the gradient w.r.t. that layer when evaluating on the given data point (need test case!)
    - implement the whole pipeline
4. ~~implement `motif_activation`~~ [link](modules/seq2pattern/_motif_activation.snakemake)
5. generate a black list of sequences where containing meaningless NNNN...
6. motif visualization

# Generate reports at `report/`

```
$ snakemake report/Type1/motif_visualization/draw_list.html
$ snakemake report/Type1/E081_motif_activation.html
$ snakemake report/Type1/E082_motif_activation.html
$ snakemake report/Type1/E081_motif_gradient.html
$ snakemake report/Type1/E082_motif_gradient.html
```
