"""
Load Dataset Module
Loads the music dataset and stores artists, tracks, and features
in a dictionary structure.
"""

import csv


class DatasetLoader:

    def __init__(self, filepath):
        self.filepath = filepath
        self.artist_music = {}

    def load_data(self):
        """
        Load CSV data and return artist_music dictionary.
        """
        with open(self.filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Handle multiple artists
                artists = row['artists'].strip("[]").replace("'", "").split(",")

                track_id = row['id']
                track_name = row['name']

                features = {
                    'acousticness': float(row['acousticness']),
                    'danceability': float(row['danceability']),
                    'energy': float(row['energy']),
                    'liveness': float(row['liveness']),
                    'loudness': float(row['loudness']),
                    'speechiness': float(row['speechiness']),
                    'tempo': float(row['tempo']),
                    'valence': float(row['valence']),
                    'popularity': int(row['popularity'])
                }

                for artist in artists:
                    artist = artist.strip()

                    if artist not in self.artist_music:
                        self.artist_music[artist] = {}

                    self.artist_music[artist][track_id] = {
                        'name': track_name,
                        'features': features
                    }

        return self.artist_music


# Test run
if __name__ == "__main__":
    loader = DatasetLoader("data.csv")
    artist_music = loader.load_data()

    print("Dataset loaded successfully")
    print(artist_music)

