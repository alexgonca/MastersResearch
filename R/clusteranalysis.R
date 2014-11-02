source("pvclust.R")
source("pvclust-internal.R")
squared_euclidean <- function(x, ...) {
	res <- dist(as.matrix(t(x)))^2
	attr(res, "method") <- "squared_euclidean"
	return(res)
}
mydata = read.csv("/home/alex/content analysis - export.csv",row.names="article")
mydata
fit <- pvclust(t(mydata), method.hclust="ward", method.dist=squared_euclidean)
png(file="dendrogram.png",width=3000,height=3000)
plot(fit)
dev.off()