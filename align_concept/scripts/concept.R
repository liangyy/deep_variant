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
  index <- 1 : dim(score)[2]
  # index <- index[!is.na(score[1,])]
  if(feature %in% c('HelT', 'Roll')) {
    index <- index + 0.5
  }
  # score <- score[!is.na(score)]
  h5write(t(score), opt$out, paste(feature, 'score', sep = '/'))  # Notice that rhdf5 save the transposed matrix, so this operation makes sure that it is consistent with what we expect 
  h5write(index, opt$out, paste(feature, 'index', sep = '/'))
  cmd <- paste('rm', paste(filename, feature, sep = '.'))
  system(cmd)
}
H5close()
