import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import song_recommendation
import os

from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances
from kneed import KneeLocator
from IPython.display import display
from dotenv import load_dotenv

def main(song, artist, number):
    data = pd.read_csv('data/data.csv')

#get rid of strings
    data1 = data.drop(['artists', 'id', 'name', 'release_date'], axis=1)

#PCA
# pca = PCA(n_components = 2)
# pca.fit(data1)
# X_reduced = pca.transform(data1)

# #scale data
# scaler = preprocessing.StandardScaler().fit(X_reduced)
# X_scaled = scaler.transform(X_reduced)
#X_test_scaled = scaler.transform(X_test)


# test kmeans for 20 clusters to get inertia
# squared_error = []
# for i in range (1, 21):
#   kmeans = KMeans(n_clusters = i, random_state=49)
#   kmeans.fit(X_scaled)
#   squared_error.append(kmeans.inertia_)
#   #print(kmeans.cluster_centers_)

#find knee for kmean squared error
# kneedle = KneeLocator(range(1, 21), squared_error, curve='convex', direction='decreasing')
# optimal_k = kneedle.elbow
# print(squared_error)

# make a plot of squared error (y-axis) vs number of cluster (x-axis)
# plt.plot(range(1, 21), squared_error)
# plt.vlines(optimal_k, plt.ylim()[0], plt.ylim()[1], linestyles='dashed')
# plt.xlabel('Number of cluster')
# plt.ylabel('Squared error')
# plt.show()
#plot
# plt.show()
# print(optimal_k)

#kmeans clustering
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(data1)
    song_cluster_labels = kmeans.predict(data1)
    data['cluster_label'] = song_cluster_labels

#add cluster_label column

#plot clusters
# projection = pd.DataFrame(columns=['x', 'y'], data=X_reduced)
# projection['title'] = data['name']
# projection['cluster'] = data['cluster_label']
# projection['artists'] = data['artists']
# fig = px.scatter(
#     projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'title', 'artists'])
# fig.show()







    song = song_recommendation.find_song(song, artist)
    song_recs = song_recommendation.rec_song(song, kmeans, number)
    return song_recs
    