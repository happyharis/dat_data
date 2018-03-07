# Hierarchical Clustering

# Importing the Mall dataset
dataset = read.csv('Mall_Customers.csv')
x = dataset[4:5]

# Using the dendrogram to predict the number of clusters
dendrogram = hclust(dist(x, method = 'euclidean'),
                    method = 'ward.D')
plot(dendrogram,
     main = paste('Dendrogram'),
     xlab = 'Customers',
     ylab = 'Euclidean Distance')

# Fitting hierarchical clustering to the mall dataset
hc = hclust(dist(x, method = 'euclidean'),method = 'ward.D')
y_hc = cutree(hc, 5)

# Visualising the clusters
library(cluster)
clusplot(dataset,
         y_hc,
         lines = 0,
         shade = TRUE,
         color = TRUE,
         labels= 2,
         plotchar = FALSE,
         span = TRUE,
         main = paste('Clusters of customers'),
         xlab = 'Annual Income',
         ylab = 'Spending Score')
