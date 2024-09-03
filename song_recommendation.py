import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import spotipy

from sklearn.metrics.pairwise import euclidean_distances
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.decomposition import PCA
from IPython.display import display

#sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ["SPOTIFY_CLIENT_ID"], client_secret=os.environ["SPOTIFY_CLIENT_SECRET"]))


data = pd.read_csv('data/data.csv')
data.iloc[1:, :]

def find_song(song, artist):
    """
    has_song = False
    has_artist = False
    test_artist = ""
    for index, row in data.iterrows():
        if row['name'] == song:
            has_song = True
            if artist in row['artists']:
                has_artist = True
                test_artist = artist
                return row"""
    return data[(data['name'] == song) & (data['artists'].str.contains(artist))]



def rec_song(song, kmeans, n):
    artist = song['artists'].iloc[0]
    name = song['name'].iloc[0]
    #display(data2)
    display(song)

    # #PCA
    # pca = PCA(n_components = 2)
    # pca.fit(data1)
    # X_reduced = pca.transform(data1)

    #scale data
    # scaler = preprocessing.StandardScaler().fit(X_reduced)
    # X_scaled = scaler.transform(X_reduced)
    #X_test_scaled = scaler.transform(X_test)
    #cluster_points = data.merge(song, on='cluster_label')
    cluster_points = data[data['cluster_label'] == song['cluster_label'].iloc[0]]
    display(cluster_points)
    cluster_points = cluster_points[((cluster_points['name'] != name) & (cluster_points['artists'] != artist))]
    data2 = song.drop(['artists', 'id', 'name', 'release_date', 'year', 'duration_ms', 'explicit', 'popularity'], axis=1)
    cluster_points2 =   cluster_points.drop(['artists', 'id', 'name', 'release_date', 'year', 'duration_ms', 'explicit', 'popularity'], axis=1)
    cluster_points2 = cluster_points2.reset_index(drop = True)
    display(cluster_points2)
    distances = euclidean_distances(data2.values, cluster_points2.values).flatten()
    print(distances)
    #filtered_points = cluster_points[cluster_points['genre'] != genre]
    # print(genre_filtered_points)
    #display(cluster_points)



    # Find the closest point with a different genre
    print(cluster_points2.index)
    song_ids = ""
    for i in range(0, n):
      closest_point_index = np.argmin(distances[cluster_points2.index])
      print(closest_point_index)
      distances = np.delete(distances, closest_point_index)
      cluster_points2 = cluster_points2.drop(closest_point_index, axis=0)
      cluster_points2 = cluster_points2.reset_index(drop = True)
      display(cluster_points.iloc[closest_point_index])
      song_ids += cluster_points.iloc[closest_point_index]['id'] + ","
    return song_ids
    
    

    


