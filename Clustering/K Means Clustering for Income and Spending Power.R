# K-means Clustering

# Import of Dataset
dataset <- read.csv('Mall_Customers.csv')
x <- dataset[4:5]

# Using the elbow method to find the optimal number of clusters
set.seed(6)
wcss <- vector()
for (i in 1:10) {wcss[i] <- sum(kmeans(x, i)$withinss)}
plot(1:10, wcss, type = "b", main = paste('Clusters of clients'), xlab = "Number of Clusters", ylab = "WCSS")

# Applying k-means to the mall dataset
set.seed(29)
kmeans = kmeans(x = dataset, centers = 5)
y_kmeans = kmeans$cluster

# Visualising the Clusters
library(cluster)
clusplot(x,
         y_kmeans,
         lines = 0,
         shade = TRUE,
         color = TRUE,
         labels = 2,
         plotchar = FALSE,
         span = TRUE,
         main = paste('Clusters of clients'),
         xlab = 'Annual Income',
         ylab = 'Spending Score')
