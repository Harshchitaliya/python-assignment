"""
Similarity Module
Computes similarity between tracks and artists
using different distance / similarity measures.
"""

import math
import random


class SimilarityCalculator:

    def __init__(self, artist_music):
        """
        artist_music: dictionary created by DatasetLoader
        """
        self.artist_music = artist_music

    # --------------------------------------------------
    # Helper methods
    # --------------------------------------------------

    def _get_track_features(self, track_id):
        """
        Return feature vector for a given track_id
        """
        for artist in self.artist_music:
            if track_id in self.artist_music[artist]:
                return list(self.artist_music[artist][track_id]['features'].values())
        return None

    def _get_artist_average_features(self, artist_name):
        """
        Compute average feature vector for an artist
        """
        if artist_name not in self.artist_music:
            return None

        feature_lists = []

        for track in self.artist_music[artist_name].values():
            feature_lists.append(list(track['features'].values()))

        # Average each feature
        avg_features = []
        for i in range(len(feature_lists[0])):
            avg = sum(f[i] for f in feature_lists) / len(feature_lists)
            avg_features.append(avg)

        return avg_features

    # --------------------------------------------------
    # Similarity metrics
    # --------------------------------------------------

    def euclidean_similarity(self, v1, v2):
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))
        return 1 / (1 + distance)

    def manhattan_similarity(self, v1, v2):
        distance = sum(abs(a - b) for a, b in zip(v1, v2))
        return 1 / (1 + distance)

    def cosine_similarity(self, v1, v2):
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_v1 = math.sqrt(sum(a ** 2 for a in v1))
        norm_v2 = math.sqrt(sum(b ** 2 for b in v2))

        if norm_v1 == 0 or norm_v2 == 0:
            return 0

        return dot_product / (norm_v1 * norm_v2)

    def pearson_similarity(self, v1, v2):
        mean1 = sum(v1) / len(v1)
        mean2 = sum(v2) / len(v2)

        num = sum((a - mean1) * (b - mean2) for a, b in zip(v1, v2))
        den1 = math.sqrt(sum((a - mean1) ** 2 for a in v1))
        den2 = math.sqrt(sum((b - mean2) ** 2 for b in v2))

        if den1 == 0 or den2 == 0:
            return 0

        return num / (den1 * den2)

    # --------------------------------------------------
    # Track similarity
    # --------------------------------------------------

    def track_similarity(self, track_id_1, track_id_2, similarity_function):
        v1 = self._get_track_features(track_id_1)
        v2 = self._get_track_features(track_id_2)

        if v1 is None or v2 is None:
            return None

        return similarity_function(v1, v2)

    # --------------------------------------------------
    # Artist similarity
    # --------------------------------------------------

    def artist_similarity(self, artist_1, artist_2, similarity_function):
        v1 = self._get_artist_average_features(artist_1)
        v2 = self._get_artist_average_features(artist_2)

        if v1 is None or v2 is None:
            return None

        return similarity_function(v1, v2)

    # --------------------------------------------------
    # Ranking similar artists (TOP 5)
    # --------------------------------------------------

    def top_5_similar_artists(self, artist_name, similarity_function, threshold=0.8):
        results = []

        for other_artist in self.artist_music:
            if other_artist == artist_name:
                continue

            score = self.artist_similarity(artist_name, other_artist, similarity_function)

            if score is not None and score >= threshold:
                results.append((other_artist, score))

        # Sort by similarity score (descending)
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:5]

    # --------------------------------------------------
    # Recommendations (Spotify-style)
    # --------------------------------------------------

    def recommend_artists(self, artist_name, similarity_function, n=10):
        similar_artists = self.top_5_similar_artists(
            artist_name, similarity_function, threshold=0
        )

        if not similar_artists:
            return []

        # Random selection (OOP idea mentioned by lecturer)
        recommendations = random.sample(
            similar_artists,
            min(len(similar_artists), n)
        )

        return recommendations
