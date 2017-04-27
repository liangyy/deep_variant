This snakemake pipeline takes a collection of fastq files as input and output the predicted scores for observed
allelic imbalance sites (may be added balance site as well). The steps are stated as follow:

1. fastq -> bam (aligner: bwa)
2. bam -> pileup (bamtools)
3. call variants (VarScan 2)
4. QC (allele freq distribution, peaked at 0.5 if sample has good quality)
5. infer imbalance (Fisher's exact test)
6. summarize extracted variants (number of imbalanced variant biased towards ref/alt; ratio of imbalanced versus balanced)
