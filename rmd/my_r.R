read_gz_url <- function(myurl){
    con <- gzcon(url(myurl))
    txt <- readLines(con)
    return(textConnection(txt))
}

read_feather_url <- function(myurl){
    download.file(myurl, '../data/temp', method = 'wget', quiet = TRUE, mode = "w", cacheOK = TRUE, extra = getOption("download.file.extra"))
    score <- read_feather('../data/temp')
    file.remove('../data/temp')
    return(score)
}