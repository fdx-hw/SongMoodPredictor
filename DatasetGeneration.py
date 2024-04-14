#5.1 Data Scraping Using Spotify API

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import math
from spotipy import util

# Spotify API credentials
client_id = 'e1c2d91fd9684a3cb5f07f7fe8520f57'
client_secret = '57a52618f7ab4c6e88a28cf1b1961f02'
redirect_uri = 'http://localhost:5000/callback'
username = 'g094fs46zt7i1qjpub6ppiy5z'

# Authenticate with Spotify API
scope = 'user-library-read'
token = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, username=username)
sp = spotipy.Spotify(auth_manager=token, requests_timeout=20)

features_for_mood = ['energy', 'liveness', 'tempo', 'speechiness',
                     'acousticness', 'instrumentalness', 'danceability', 'duration_ms',
                     'loudness', 'valence']

def get_track_features(track_ids, track_links, spotify):

    #initialized chunk size for scraping playlists
    chunk_size = 50
    num_chunks = int(math.ceil(len(track_ids) / float(chunk_size)))
    features_add = []

    for i in range(num_chunks):
        chunk_track_ids = track_ids[i * chunk_size:min((i + 1) * chunk_size, len(track_ids))]

        # Initialized offset 
        offset = 0
        while offset < len(chunk_track_ids):
            # Fetches track IDs, audio features and the tracks according to the chunk size from the playlist
            chunk_ids = chunk_track_ids[offset:offset + chunk_size]
            chunk_features = spotify.audio_features(tracks=chunk_ids)
            chunk_tracks = spotify.tracks(tracks=chunk_ids)['tracks']

            for feature, track_info, track_uri, track_link in zip(chunk_features, chunk_tracks, chunk_ids, track_links[offset:offset + chunk_size]):
                feature['name'] = track_info['name']
                feature['artist'] = track_info['artists'][0]['name']
                feature['uri'] = track_uri
                feature['track_link'] = track_link

            features_add.extend(chunk_features)

            #Increases offset by chunk size
            offset += chunk_size
            # Added timed delay to prevent reaching the request limit
            time.sleep(0.1)

    features_df = pd.DataFrame(features_add).drop(['id', 'analysis_url', 'key', 'mode', 'time_signature',
                                                   'track_href', 'type', 'uri'], axis=1)
    features_df = features_df[features_for_mood + ['name', 'artist', 'track_link']]
    return features_df

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print(" %d %s %s" % (i, track['artists'][0]['name'], track['name']))

#The uncommented links below are the links to the master playlists created for each mood which consists of the songs gathered from other user curated mood playlists.
#The commented links below were the user curated playlists for each mood from which the songs were collected and added to the master playlists
playlists = {
    'Calm': ["https://open.spotify.com/playlist/3VR9Q5hdGq5D8F7KEJa60K?si=61602184bd83405a"],
            #  "https://open.spotify.com/playlist/37i9dQZF1EIhmXwY1VouXP?si=f936ffc1c9db4feb",
            #  "https://open.spotify.com/playlist/4h2MD8T5fNW2Ss8sO5up68?si=ca8e1fc883f14334",
            #  "https://open.spotify.com/playlist/7KZVlzeVPxU1LmCWAYpVNs?si=f7eff5f2a20140f0",
            #  "https://open.spotify.com/playlist/45Frz6YTusqtvatr4of8KU?si=6b1a9e6c791a401f"]
    'Sad':  ["https://open.spotify.com/playlist/1vI8a6UVWlbXvGqKcO2Jko?si=2b8e725d6f18469b",
            "https://open.spotify.com/playlist/6eOYvcF9QgbmfAlI7EDpxd?si=b3e546d98e974fe6",
            "https://open.spotify.com/playlist/5PTWBLG8sBnM8lZEgQCFk6?si=b3ac3e214ae5435b"],
    #         "https://open.spotify.com/playlist/5DVUEqRL1EV8I9n65eBaAw?si=47769a9133a740ae",
    #         "https://open.spotify.com/playlist/37i9dQZF1EIg6gLNLe52Bd?si=e40c257846f04630",
    #         "https://open.spotify.com/playlist/37i9dQZF1DWSqBruwoIXkA?si=367e6ffc529840c1",
    #         "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1?si=fd9db5948cab4ada",
    #         "https://open.spotify.com/playlist/1lulj4sd1Q5oXBoZbV82vb?si=dfe02e0b70da4f71",
    #         "https://open.spotify.com/playlist/4kPr5JnmXhy9OxewtmylVI?si=3181d208212046a0",
    #         "https://open.spotify.com/playlist/6nxPNnmSE0d5WlplUsa5L3?si=2ce3bcf41e0141dc"]
    'Angry':  ["https://open.spotify.com/playlist/4Mjg9IX4OYT9GuVGP24ph6?si=f8312ea6428c477c"],
    #            "https://open.spotify.com/playlist/7rthAUYUFcbEeC8NS8Wh42?si=ab7f353f5f2847b3",
    #            "https://open.spotify.com/playlist/2F6JtyDh4aHd77mfcxrz4R?si=6e181fdaf09c464c",
    #            "https://open.spotify.com/playlist/609gQW5ztNwAkKnoZplkao?si=963e439e495f4bd9",
    #            "https://open.spotify.com/playlist/4NX7OGpc4HVFYmB2hNcGpV?si=caf24db2312a409c",
    #            "https://open.spotify.com/playlist/37i9dQZF1EIdPM7mGygW5M?si=8999b4c79d3c4363",
    #            "https://open.spotify.com/playlist/2I3Mt48eHvNinZtiOcwfzF?si=d08905cc91ec4f1a",
    #            "https://open.spotify.com/playlist/1xdEaBisiJRDotBWbQGmnd?si=b1300db3fde744aa",
    #            "https://open.spotify.com/playlist/4GCjTivoG40uCM2nPvWofg?si=63429dc09f904bbb"],
    'Happy': ["https://open.spotify.com/playlist/4TUJNhzPhT68za9Y7HQmwT?si=e7f4ac3403284a50"]
    #           "https://open.spotify.com/playlist/4AnAUkQNrLKlJCInZGSXRO?si=9846e647548d4026",
    #           "https://open.spotify.com/playlist/37i9dQZF1DWSf2RDTDayIx?si=391caedbdba649bb",
    #           "https://open.spotify.com/playlist/4Fh0313D3PitYzICKHhZ7r?si=1b9ecbc3904d42e7",
    #           "https://open.spotify.com/playlist/0okKcRyYEwq8guFxzAPtlB?si=77a0ac02c5b345c1"]
}

all_tracks = pd.DataFrame()

for mood, links in playlists.items():
    mood_tracks = pd.DataFrame()

    for link in links:
        id = link.split('/')[-1].split('?')[0] 

        # Initialize the offset for iterating through the 100 song limit for each playlist
        offset = 0

        while True:
            try:
                # Fetch the tracks of the playlist
                pl_tracks = sp.playlist_tracks(id, offset=offset)['items']
            except:
                break

            if not pl_tracks:
                break

            # Extract track IDs and links from the fetched playlist tracks
            ids = [foo['track']['id'] for foo in pl_tracks]
            track_links = [foo['track']['external_urls']['spotify'] for foo in pl_tracks]

            # get_track_features function to get audio features for each track
            features = get_track_features(ids, track_links, sp)

            features['id'] = ids
            features['mood'] = mood
            mood_tracks = pd.concat([mood_tracks, features], ignore_index=True)

            # Increment the offset by the 100 song limit to start retrieving the next set of the tracks from the playlist  
            offset += len(pl_tracks)

    # Concatenate the tracks obtained from mood playlists to final dataframe
    all_tracks = pd.concat([all_tracks, mood_tracks], ignore_index=True)

# Save the dataFrame to a CSV file
all_tracks.to_csv('combined_moods_bigger.csv', index=False)