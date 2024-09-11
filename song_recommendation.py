import numpy as np
import pandas as pd
import spotify

from sklearn.metrics.pairwise import euclidean_distances



def find_song(song, artist, data):

    song1 = data[(data['name']==song)]
    artist1 = song1[(song1['artists'].str.contains(artist, regex = False))]
    print(artist1.shape[0])
    #checks if artist exists in data
    if artist1.shape[0] != 0:
        return data[(data['name'] == song) & (data['artists'].str.contains(artist, regex = False))], True
    
    else: 
        song_result = spotify.search_for_song(song, artist)
        #tests
        #print(song_result)
        #print(song_result.keys())
        #print(song_result.get('tracks').keys())
        id = song_result.get('tracks').get("items")[0].get("id")
        song_data = spotify.get_audio_features(id)
        #print(song_data)

        #PROCESSING SPOTIFY AUDIO FEATURES to match our dataset
        song_data = song_data.drop(['analysis_url', 'time_signature', 'track_href', 'type', 'uri'], axis=1)
        acousticness = song_data['acousticness']
        danceability = song_data['danceability']
        duration_ms = song_data['duration_ms']
        energy = song_data['energy']
        new_id = song_data['id']
        instrumentalness = song_data['instrumentalness']
        key = song_data['key']
        liveness = song_data['liveness']
        loudness = song_data['loudness']
        mode = song_data['mode']
        speechiness = song_data['speechiness']
        tempo = song_data['tempo']
        valence = song_data['valence']

        #new dataframe in order, not sure if order matters but just in case
        new_song_data = pd.DataFrame()
        new_song_data['valence'] = valence
        new_song_data['acousticness'] = acousticness
        new_song_data['artists'] = artist
        new_song_data['danceability'] = danceability
        new_song_data['duration_ms'] = duration_ms
        new_song_data['energy'] = energy
        new_song_data['id'] = new_id
        new_song_data['instrumentalness'] = instrumentalness
        new_song_data['key'] = key
        new_song_data['liveness'] = liveness
        new_song_data['loudness'] = loudness
        new_song_data['mode'] = mode
        new_song_data['name'] = song
        new_song_data['speechiness'] = speechiness
        new_song_data['tempo'] = tempo
        return new_song_data, False


        
       



def rec_song(song, model, n, data):
    artist = song['artists'].iloc[0]
    name = song['name'].iloc[0]
    #display(data2)

    #PCA/scaling optional, so far looks better without
    # pca = PCA(n_components = 2)
    # pca.fit(data1)
    # X_reduced = pca.transform(data1)

    #scale data
    # scaler = preprocessing.StandardScaler().fit(X_reduced)
    # X_scaled = scaler.transform(X_reduced)
    #X_test_scaled = scaler.transform(X_test)
    #cluster_points = data.merge(song, on='cluster_label')
    
    cluster_points = data[data['cluster_label'] == song['cluster_label'].iloc[0]]
    cluster_points = cluster_points[((cluster_points['name'] != name) & (cluster_points['artists'] != artist))]
    cluster_points2 =   cluster_points.drop(['artists', 'name', 'id','release_date', 'year', 'explicit', 'popularity', 'duration_ms'], axis=1)
    cluster_points2 = cluster_points2.reset_index(drop = True)
    song = song.drop(["artists",'name'], axis=1)
    #print(song)
    #print(cluster_points2)
    distances = euclidean_distances(song.values, cluster_points2.values).flatten()
    #print("test1")


    # Find the ids of the closest n points
    song_ids = ""
    for i in range(0, n):
      closest_point_index = np.argmin(distances[cluster_points2.index])
      distances = np.delete(distances, closest_point_index)
      cluster_points2 = cluster_points2.drop(closest_point_index, axis=0)
      cluster_points2 = cluster_points2.reset_index(drop = True)
      song_ids += cluster_points.iloc[closest_point_index]['id'] + ","

    return song_ids
    
    

    


