library("optparse")

option_list <- list(
  make_option(c("-f", "--file"), type = "character", default = NULL,
              help = "Input fasta file", metavar = "character"),
	make_option(c("-o", "--out"), type = "character", default = NULL,
              help = "Output hdf5 file", metavar = "character")
);

opt_parser <- OptionParser(option_list=option_list)
opt <- parse_args(opt_parser)

library(DNAshapeR)
library(rhdf5)
filename <- opt$file
pred <- getShape(filename)
features <- c('MGW', 'HelT', 'ProT', 'Roll', 'EP')
h5createFile(opt$out)

for(feature in features) {
  h5createGroup(opt$out, feature)
  score <- pred[[feature]]
  index <- 1 : dim(score)[1]
  index <- index[!is.na(score)]
  score <- score[!is.na(score)]
  h5write(score, opt$out, paste(feature, 'score', sep = '/'))
  h5write(index, opt$out, paste(feature, 'index', sep = '/'))
  cmd <- paste('rm', paste(filname, feature, sep = '.'))
  system(cmd)
}
H5close()
