import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

data = pd.read_csv('data/data.csv')
genre_data = pd.read_csv('data/data_by_genres.csv')

#PCA
data = data.select_dtypes(exclude = [object])
pca = PCA(n_components = 2)
pca.fit(data)
X_reduced = pca.transform(data)


print(X_reduced)

#represent data
plt.scatter(X_reduced[:,0], X_reduced[:, 1])
#plt.show()

#kmeans test
kmeans = KMeans(n_clusters=10)
kmeans.fit(X_reduced)
print(kmeans.cluster_centers_)
print(kmeans.labels_)

def plot_kmeans(X, kmeans, ax=None):
    if ax is None:
        ax = plt.gca()
    ax.scatter(X[:,0],X[:,1], c=kmeans.labels_, cmap='rainbow')
    centers = kmeans.cluster_centers_
    ax.scatter(centers[:,0], centers[:,1], c=np.arange(centers.shape[0]),
               marker='x', s=100, cmap='rainbow')

#plot_kmeans(X_reduced, kmeans)
#plt.show()

# kmeans for 10 clusters
squared_error = []
for i in range (2900, 3000):
  kmeans = KMeans(n_clusters = i)
  kmeans.fit(X_reduced)
  squared_error.append(kmeans.inertia_)
  print(kmeans.cluster_centers_)

print(squared_error)

# make a plot of squared error (y-axis) vs number of cluster (x-axis)
plt.plot(range(2900, 3001), squared_error)
plt.xlabel('Number of cluster')
plt.ylabel('Squared error')
plt.show()