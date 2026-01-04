"""
Statistics Module
Implements functions for statistical analysis of dataset features.
Supports mean, mode, standard deviation, minimum, maximum, and variance.
"""

import math
from collections import Counter


class StatsAnalyzer:
    def __init__(self, artist_music: dict):
        """
        artist_music is the dict returned by DatasetLoader.load_data()
        """
        self.artist_music = artist_music

    # ---------- Helpers ----------
    def _all_feature_values(self, feature_name: str):
        """
        Collect all values for a given feature across all artists and tracks.
        Returns a list of numbers.
        """
        values = []
        for artist_tracks in self.artist_music.values():
            for track_data in artist_tracks.values():
                features = track_data.get("features", {})
                if feature_name in features:
                    values.append(features[feature_name])
        return values

    def _mean(self, values):
        return sum(values) / len(values) if values else None

    def _min(self, values):
        return min(values) if values else None

    def _max(self, values):
        return max(values) if values else None

    def _variance(self, values, sample: bool = False):
        """
        Variance:
        - population variance if sample=False  (divide by n)
        - sample variance if sample=True       (divide by n-1)
        """
        n = len(values)
        if n == 0:
            return None
        if sample and n < 2:
            return None

        m = self._mean(values)
        total = sum((x - m) ** 2 for x in values)
        return total / (n - 1 if sample else n)

    def _std_dev(self, values, sample: bool = False):
        var = self._variance(values, sample=sample)
        return math.sqrt(var) if var is not None else None

    def _mode(self, values):
        """
        Mode:
        - Returns a single value if there is a clear mode
        - Returns None if there is no mode (all equally common)
        - Returns list if multiple modes (tie)
        """
        if not values:
            return None

        counts = Counter(values)
        max_count = max(counts.values())

        # If every value occurs equally often, there's no mode
        if len(set(counts.values())) == 1:
            return None

        modes = [val for val, c in counts.items() if c == max_count]
        return modes[0] if len(modes) == 1 else modes

    # ---------- Public API ----------
    def feature_summary(self, feature_name: str, sample_std: bool = False):
        """
        Returns a dictionary summary for a feature across the entire dataset.
        sample_std controls whether variance/std-dev are sample or population.
        """
        values = self._all_feature_values(feature_name)

        return {
            "count": len(values),
            "mean": self._mean(values),
            "mode": self._mode(values),
            "min": self._min(values),
            "max": self._max(values),
            "variance": self._variance(values, sample=sample_std),
            "std_dev": self._std_dev(values, sample=sample_std),
        }



# ---------- Test Run ----------
if __name__ == "__main__":
    # Example usage with your loader
    from load_dataset import DatasetLoader  # if your file is named load_dataset.py

    loader = DatasetLoader("data.csv")
    artist_music = loader.load_data()
    print(artist_music)
    analyzer = StatsAnalyzer(artist_music)

    # Single feature summary
    print("Danceability summary:")
    print(analyzer.feature_summary("danceability"))

    # All features summary
    print("\nAll features summary:")
    all_stats = analyzer.all_features_summary()
    for feat, stats in all_stats.items():
        print(feat, "=>", stats)
