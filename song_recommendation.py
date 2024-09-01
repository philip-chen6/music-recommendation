import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances

data = pd.read_csv('data/data.csv')
data.iloc[1:, :]

def find_song(song, artist):
    return data[data["name"] == song]

def rec_song(song, genre, kmeans):
    point = data[song]
    cluster_label = kmeans.predict([point])[0]
    cluster_points = data[kmeans.labels_ == cluster_label]
    diff_genre = False
    i = 0
    while diff_genre == False:
        distances = euclidean_distances([point], cluster_points)[i]
        distances[distances == 0] = np.inf
        closest_point_index = np.argmin(distances)
        closest_point = cluster_points[closest_point_index]   
        if closest_point['genre'] == genre:
            diff_genre = True
        i += 1


    


