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
