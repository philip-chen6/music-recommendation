import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import song_recommendation

from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances
from kneed import KneeLocator
from IPython.display import display
from dotenv import load_dotenv

def main(song, artist, number, model_choice):
    data = pd.read_csv('data/data.csv')

#get rid of strings
    data1 = data.drop(['artists', 'id', 'name', 'release_date', 'year', 'duration_ms', 'explicit', 'popularity'], axis=1)

    #PCA
    # pca = PCA(n_components = 2)
    # pca.fit(data1)
    # data1 = pca.transform(data1)
    
    #scale data
    scaler = preprocessing.StandardScaler().fit(data1)
    data1 = scaler.transform(data1)
    #X_test_scaled = scaler.transform(X_test)

    if model_choice == "KMeans":
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

    #kmeans clustering, predict and add column of cluster labels
        model = KMeans(n_clusters=5)
        model.fit(data1)
        song_cluster_labels = model.predict(data1)
        data['cluster_label'] = song_cluster_labels

    #plot clusters
    # projection = pd.DataFrame(columns=['x', 'y'], data=X_reduced)
    # projection['title'] = data['name']
    # projection['cluster'] = data['cluster_label']
    # projection['artists'] = data['artists']
    # fig = px.scatter(
    #     projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'title', 'artists'])
    # fig.show()

    elif model_choice == "GMM":
        # AIC = []
        # BIC = []
        # for k in range(1,11):
        #     gaussian = GaussianMixture(n_components = k).fit(data1)
        #     AIC.append(gaussian.aic(data1))
        #     BIC.append(gaussian.bic(data1))

        # plot the results of AIC vs. number of clusters and BIC vs. number of clusters
        # plt.plot(range(1,11), AIC, label='AIC')
        # plt.plot(range(1,11), BIC, label='BIC')
        # plt.legend()
        k = 10 # best num of clusters
        model = GaussianMixture(n_components = k).fit(data1)
        song_cluster_labels = model.predict(data1)
        data['cluster_label'] = song_cluster_labels

    #get individual song data and if its in the dataset   
    #COME HERE
    song_data, is_in_dataset, genres = song_recommendation.find_song(song, artist, data)
    if is_in_dataset == False:
        # artist = song_data['artists'].iloc[0]
        # name = song_data['name'].iloc[0]
        song_data1 = song_data.drop(['artists', 'id', 'name', 'duration_ms'  ], axis=1)
        song_data = song_data.drop(['id', 'duration_ms'], axis=1)
        
        # pca1 = PCA(n_components = 2, svd_solver='full')
        # pca1.fit(song_data1)
        # song_data1 = pca1.transform(song_data1)
        
        scaler = preprocessing.StandardScaler().fit(song_data1)
        song_data1 = scaler.transform(song_data1)

        song_cluster_label = model.predict(song_data1)
        song_data['cluster_label'] = song_cluster_label
        # song_data['artists'] = artist
        # song_data['name'] = name
        
    else:
        print(song_data)
        artist = song_data['artists'].iloc[0]
        name = song_data['name'].iloc[0]
        song_data = song_data.drop(['artists', 'id', 'name', 'duration_ms', 'release_date', 'year', 'explicit', 'popularity'], axis=1)
        
        song_data['artists'] = artist
        song_data['name'] = name

    song_recs = song_recommendation.rec_song(song_data, model, number,data, genres)

    return song_recs
    