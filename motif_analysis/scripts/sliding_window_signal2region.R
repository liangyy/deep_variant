#!/usr/bin/env Rscript
library("optparse")
library(feather)

option_list = list(
    make_option(c("-f", "--file"), type="character", default=NULL,
                help="dataset file name", metavar="character"),
    make_option(c("-o", "--out"), type="character", default="out.txt",
                help="output file name [default= %default]", metavar="character"),
    make_option(c('-m', '--extract_mode'), type='character', default='positive',
                help='match the mode with the input file (positive|negative) or set it to random', metavar='character'),
    make_option(c('-q', '--quantile'), type='double', default=0.0001)
);

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);


pos <- read_feather(opt$file)
if(opt$extract_mode == 'positive'){
    threshold <- quantile(unlist(pos), opt$quantile)
    seq <- c()
    position <- c()
    for(x in 1 : nrow(pos)){
        signal <- pos[x,]
        pass.idx <- which(signal <= threshold)
        seq <- c(seq, rep(x, length(pass.idx)))
        position <- c(position, pass.idx)
    }
}else if(opt$extract_mode == 'negative'){
    threshold <- quantile(unlist(pos), 1 - opt$quantile)
    seq <- c()
    position <- c()
    for(x in 1 : nrow(pos)){
        signal <- pos[x,]
        pass.idx <- which(signal >= threshold)
        seq <- c(seq, rep(x, length(pass.idx)))
        position <- c(position, pass.idx)
    }
}else if(opt$extract_mode == 'random'){
    n <- opt$quantile * nrow(pos) * ncol(pos)
    seq <- c()
    position <- c()
    seq <- sample(1 : nrow(pos), n, replace=T)
    position <- sample(1 : ncol(pos), n, replace=T)
}

out <- data.frame(seq_id = seq, pos_id = position)
write.table(out, file = opt$out, quote = F, row.names = F, col.names = T)
