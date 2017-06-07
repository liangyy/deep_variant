ai_deepsea_save_plot <- function(info, p, name, path, plots, folder, w, h){
    filename <- paste(paste(c(info, name), collapse = '_'), '.png', sep = '')
    ggsave(filename = filename, plot = p, path = path, width = w, height = h)
    plots[[as.character(name)]] <- paste(folder, filename, sep = '/')
    plots
}

accuracy <- function(y, y_pred){
    temp <- rep(0, length(y_pred))
    temp[y_pred > 0.5] <- 1 
    return(mean(temp == y))
}

precision <- function(y, temp){
    return(sum(y == 1 & temp == 1) / sum(temp == 1))
}

recall <- function(y, temp){
    return(sum(y == 1 & temp == 1) / sum(y == 1))
}

precision.t <- function(y, y_pred){
    temp <- rep(0, length(y_pred))
    temp[y_pred > 0.5] <- 1 
    return(precision(y, temp))
    
}

precision.f <- function(y, y_pred){
    temp <- rep(0, length(y_pred))
    temp[y_pred > 0.5] <- 1 
    return(precision(1 - y, 1 - temp))
}

recall.t <- function(y, y_pred){
    temp <- rep(0, length(y_pred))
    temp[y_pred > 0.5] <- 1 
    return(recall(y, temp))
}

recall.f <- function(y, y_pred){
    temp <- rep(0, length(y_pred))
    temp[y_pred > 0.5] <- 1 
    return(recall(1 - y, 1 - temp))
}

proportion.t <- function(y){
    return(mean(y))
}

proportion.f <- function(y){
    return(1 - proportion.t(y))
}

## derived from http://www.cookbook-r.com/Graphs/Multiple_graphs_on_one_page_(ggplot2)/
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
    library(grid)
    
    # Make a list from the ... arguments and plotlist
    plots <- c(list(...), plotlist)
    
    numPlots = length(plots)
    
    # If layout is NULL, then use 'cols' to determine layout
    if (is.null(layout)) {
        # Make the panel
        # ncol: Number of columns of plots
        # nrow: Number of rows needed, calculated from # of cols
        layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                         ncol = cols, nrow = ceiling(numPlots/cols))
    }
    
    if (numPlots==1) {
        print(plots[[1]])
        
    } else {
        # Set up the page
        grid.newpage()
        pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
        
        # Make each plot, in the correct location
        for (i in 1:numPlots) {
            # Get the i,j matrix positions of the regions that contain this subplot
            matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
            
            print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                            layout.pos.col = matchidx$col))
        }
    }
}
## end

read_gz_url <- function(url_string){
  con <- gzcon(url(url_string))
  txt <- readLines(con)
  return(textConnection(txt))
}

read_feather_url <- function(url_string){
  cmd <- paste('curl', url_string, '>', 'temp.feather')
  system(cmd)
  data <- read_feather('temp.feather')
  cmd <- paste('rm', 'temp.feather')
  return(data)
}

logit <- function(p){
  return(log10(p / (1 - p)))
}

# derived from http://stackoverflow.com/questions/7549694/adding-regression-line-equation-and-r2-on-graph
lm_eqn = function(m) {
  
  l <- list(a = format(coef(m)[1], digits = 2),
            b = format(abs(coef(m)[2]), digits = 2),
            r2 = format(summary(m)$r.squared, digits = 3));
  if (length(coef(m)) == 2){
    if (coef(m)[2] >= 0)  {
      eq <- substitute(italic(y) == a + b %.% italic(x)*","~~italic(r)^2~"="~r2,l)
    } else {
      eq <- substitute(italic(y) == a - b %.% italic(x)*","~~italic(r)^2~"="~r2,l)    
    }
  }else{
    if (coef(m)[1] >= 0)  {
      eq <- substitute(italic(y) == a %.% italic(x)*","~~italic(r)^2~"="~r2,l)
    } else {
      eq <- substitute(italic(y) == a %.% italic(x)*","~~italic(r)^2~"="~r2,l)    
    }    
  }
  as.character(as.expression(eq));                 
}
# end