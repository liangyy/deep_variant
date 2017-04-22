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
