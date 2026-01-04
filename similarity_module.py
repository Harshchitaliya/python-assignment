import math


class SimilarityEngine:

    def __init__(self, artist_music):
        self.artist_music = artist_music

    def get_track_features(self, track_id):
        for artist in self.artist_music:
            tracks = self.artist_music[artist]
            if track_id in tracks:
                return tracks[track_id]["features"]
        return None

    def features_to_list(self, features):
        values = []
        for key in features:
            values.append(features[key])
        return values

    def euclidean_similarity(self, list1, list2):
        total = 0
        for i in range(len(list1)):
            total += (list1[i] - list2[i]) ** 2
        return math.sqrt(total)

    def cosine_similarity(self, list1, list2):
        dot_product = 0
        mag1 = 0
        mag2 = 0

        for i in range(len(list1)):
            dot_product += list1[i] * list2[i]
            mag1 += list1[i] ** 2
            mag2 += list2[i] ** 2

        if mag1 == 0 or mag2 == 0:
            return 0

        return dot_product / (math.sqrt(mag1) * math.sqrt(mag2))

    def pearson_similarity(self, list1, list2):
        mean1 = sum(list1) / len(list1)
        mean2 = sum(list2) / len(list2)

        top = 0
        bottom1 = 0
        bottom2 = 0

        for i in range(len(list1)):
            top += (list1[i] - mean1) * (list2[i] - mean2)
            bottom1 += (list1[i] - mean1) ** 2
            bottom2 += (list2[i] - mean2) ** 2

        if bottom1 == 0 or bottom2 == 0:
            return 0

        return top / (math.sqrt(bottom1) * math.sqrt(bottom2))

    def track_similarity(self, track1_id, track2_id, method):
        f1 = self.get_track_features(track1_id)
        f2 = self.get_track_features(track2_id)

        if f1 is None or f2 is None:
            raise ValueError("Track ID not found")

        list1 = self.features_to_list(f1)
        list2 = self.features_to_list(f2)

        if method == "euclidean":
            return self.euclidean_similarity(list1, list2)
        if method == "manhattan":
            return self.manhattan_similarity(list1, list2)
        if method == "cosine":
            return self.cosine_similarity(list1, list2)
        if method == "pearson":
            return self.pearson_similarity(list1, list2)

        raise ValueError("Invalid similarity method")

    def artist_similarity(self, artist1, artist2, method):

        def average_features(artist):
            tracks = self.artist_music.get(artist, {})
            total = None
            count = 0

            for track in tracks.values():
                features = self.features_to_list(track["features"])
                if total is None:
                    total = features
                else:
                    for i in range(len(total)):
                        total[i] += features[i]
                count += 1

            return [value / count for value in total]

        avg1 = average_features(artist1)
        avg2 = average_features(artist2)

        if method == "euclidean":
            return self.euclidean_similarity(avg1, avg2)
        if method == "manhattan":
            return self.manhattan_similarity(avg1, avg2)
        if method == "cosine":
            return self.cosine_similarity(avg1, avg2)
        if method == "pearson":
            return self.pearson_similarity(avg1, avg2)

        raise ValueError("Invalid similarity method")

    def top_5_similar_artists(self, artist, method):
        results = []

        for other_artist in self.artist_music:
            if other_artist != artist:
                score = self.artist_similarity(artist, other_artist, method)
                results.append((other_artist, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:5]
