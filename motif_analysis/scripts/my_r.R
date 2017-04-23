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


load_and_melt <- function(filename){
    pos <- read_feather(filename)
    pos$id <- 1 : (nrow(pos))
    pos.melted <- melt(pos, id.vars = 'id')
    return(list(table=pos, table.melted=pos.melted))
}

plot_motif <- function(pos.in, neg.in, motif, pvalue){
    pos.sub <- pos.in[pos.in$variable == motif,]
    neg.sub <- neg.in[neg.in$variable == motif,]
    pos.sub$label <- 'positive'
    neg.sub$label <- 'negative'
    merged.sub <- rbind(pos.sub, neg.sub)
    merged.sub$rank <- rank(merged.sub$value)
    p <- ggplot(merged.sub) + geom_histogram(aes(x = rank, fill = label), bins = 30, position='dodge') +
        facet_grid(label~.) +
        ggtitle(paste('Histogram of Activation', motif, '\n p.value = ', formatC(pvalue))) + 
        theme(title = element_text(size=3.5), text = element_text(size=3))
    return(p)
}

save_plot <- function(info, p, motif, path, plots){
    filename <- paste(paste(c(info, motif), collapse = '_'), '.png', sep = '')
    ggsave(filename = filename, plot = p, path = path, width = 3, height = 1.5)
    plots[[as.character(motif)]] <- paste(path, filename, sep = '/')
    plots
}

plot_motif_visual <- function(filename = filname, motif_idx = motif_idx){
    motif <- read_feather(filename)
    motif$Base <- c('A', 'G', 'C', 'T') # ATTENTION! This depends on now you preprocess the data
    motif.melted <- melt(motif, id.vars = 'Base')
    p <- ggplot(motif.melted, aes(x = variable, y = value, group = Base)) + geom_bar(aes(fill = Base), stat='identity', position = 'dodge') +
        geom_text(
        aes(label = Base, y = value / 2),
        position = position_dodge(0.9),
        vjust = 0
    ) + ggtitle(paste('Motif', motif_idx, sep = '.'))
    return(p)
}

compute_cor <- function(data, cond){
    data.sub <- data[data$Direction == cond, ]
    selected <- !colnames(data.sub) %in% 'Direction'
    data.sub.cor <- cor(data.sub[, selected])
    return(data.sub.cor)
}

cor_to_hist <- function(pos, instance){
    pos.cor.min <- compute_cor(pos, 'decrease')
    pos.cor.min.melted <- melt(pos.cor.min)
    pos.cor.max <- compute_cor(pos, 'increase')
    pos.cor.max.melted <- melt(pos.cor.max)
    p <- ggplot() + xlim(0, 1) +
        geom_histogram(data = pos.cor.min.melted, aes(x = value, fill = 'decrease'), bins = 30, alpha = .3) + 
        geom_histogram(data = pos.cor.max.melted, aes(x = value, fill = 'increase'), bins = 30, alpha = .3) + 
        ggtitle(paste('Histogram of the correlation btw motifs in', instance, 'samples'))
    return(p)
}

plot_gradient <- function(pos, string){
    temp.pos <- pos
    temp.pos$id <- rep(1 : (nrow(temp.pos) / 2), each = 2)
    pos.melted <- melt(temp.pos, id.vars = c('Direction', 'id'))
    p1 <- ggplot(pos.melted) + 
        geom_raster(aes(x = variable, y = id, fill = value)) + 
        scale_fill_gradient2() + ggtitle(paste('Gradient per sequence (', string, ')', sep = '')) + 
        labs(x = 'motif', y = 'sequence') + 
        facet_grid(Direction~.)
    return(p1)
}

plot_per_motif_grad_mean <- function(pos, title){
    pos.max.mean <- colMeans(pos[pos$Direction == 'increase', !colnames(pos) %in% 'Direction'])
    pos.min.mean <- colMeans(pos[pos$Direction == 'decrease', !colnames(pos) %in% 'Direction'])
    p <- ggplot() + geom_point(aes(x = pos.max.mean, y = pos.min.mean)) + 
        labs(x = 'mean of increase', y = 'mean of decrease') + 
        ggtitle(paste('Comparison btw two directions in', title, 'data'))
    motifs <- colnames(pos)[!colnames(pos) %in% 'Direction']
    motif.order <- order(pos.max.mean, decreasing = T)
    motifs.ordered <- as.character(motifs[motif.order])
    return(list(plot = p, motifs = motifs.ordered, mean.max = pos.max.mean[motif.order], mean.min = pos.min.mean[motif.order]))
}

reformat_grad <- function(pos){
    pos[,!colnames(pos) %in% 'Direction'] <- lapply(pos[,!colnames(pos) %in% 'Direction'], as.numeric)
    pos$Direction[pos$Direction == 'max'] <- 'increase'
    pos$Direction[pos$Direction == 'min'] <- 'decrease'
    return(pos)
}

plot_per_motif_grad <- function(pos, motif, title, means){
    data.sub <- pos[, c(motif, 'Direction')]
    p <- ggplot(data.sub) + geom_boxplot(aes_string(x = 'Direction', y = motif)) + 
        ggtitle(paste('Gradient of', motif, 'across', title, 'data', '\n', 'increase mean = ', formatC(means[1]), '\n', 'decrease mean = ', formatC(means[2]))) +
        theme(title = element_text(size=3.5), text = element_text(size=3))
    return(p)
}

save_plot2 <- function(info, p, motif, path, plots){
    filename <- paste(paste(c(info, motif), collapse = '_'), '.png', sep = '')
    ggsave(filename = filename, plot = p, path = path, width = 1.5, height = 2.2)
    plots[[as.character(motif)]] <- paste(path, filename, sep = '/')
    plots
}