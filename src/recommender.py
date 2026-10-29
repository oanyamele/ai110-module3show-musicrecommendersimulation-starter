
import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numeric fields to numbers."""
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["popularity"] = int(row["popularity"])
            row["mood_tags"] = [tag.strip() for tag in row["mood_tags"].split("|") if tag.strip()]

            for field in ("energy", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])

            songs.append(row)

    return songs


class ScoringStrategy:
    """Shared weighted scoring for a song's core preferences."""
    genre_weight = 1.0
    mood_weight = 1.0
    energy_weight = 2.0

    def score_core(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if song["genre"] == user_prefs["favorite_genre"]:
            score += self.genre_weight
            reasons.append(f"genre match (+{self.genre_weight:.1f})")

        if song["mood"] == user_prefs["favorite_mood"]:
            score += self.mood_weight
            reasons.append(f"mood match (+{self.mood_weight:.1f})")

        energy_points = self.energy_weight * (
            1.0 - abs(song["energy"] - user_prefs["target_energy"])
        )
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")
        return score, reasons


class BalancedScoringStrategy(ScoringStrategy):
    """Use the project's current genre, mood, and energy weights."""


class GenreFirstScoringStrategy(ScoringStrategy):
    """Give genre matches more weight than mood or energy similarity."""
    genre_weight = 2.0
    mood_weight = 0.5
    energy_weight = 1.0


class EnergyFocusedScoringStrategy(ScoringStrategy):
    """Give energy similarity more weight than genre or mood matches."""
    genre_weight = 0.5
    mood_weight = 0.5
    energy_weight = 3.0


SCORING_STRATEGIES = {
    "balanced": BalancedScoringStrategy(),
    "genre-first": GenreFirstScoringStrategy(),
    "energy-focused": EnergyFocusedScoringStrategy(),
}


def _get_scoring_strategy(mode: str) -> ScoringStrategy:
    strategy_name = mode.strip().lower().replace("_", "-")
    strategy = SCORING_STRATEGIES.get(strategy_name)
    if strategy is None:
        valid_modes = ", ".join(SCORING_STRATEGIES)
        raise ValueError(f"Unknown scoring mode {mode!r}. Choose from: {valid_modes}.")
    return strategy


def _add_advanced_feature_scores(
    user_prefs: Dict,
    song: Dict,
    score: float,
    reasons: List[str],
) -> Tuple[float, List[str]]:
    """Apply the same bounded optional feature bonuses to every mode."""
    feature_weight = 0.25
    popularity = song.get("popularity")
    if popularity is not None:
        popularity_points = feature_weight * max(0.0, min(float(popularity), 100.0)) / 100.0
        score += popularity_points
        reasons.append(f"popularity prior (+{popularity_points:.2f})")

    desired_tags = user_prefs.get("desired_mood_tags") or []
    if isinstance(desired_tags, str):
        desired_tags = [desired_tags]
    song_tags = song.get("mood_tags") or []
    if isinstance(song_tags, str):
        song_tags = song_tags.split("|")
    desired_tags = {tag.strip().lower() for tag in desired_tags if tag.strip()}
    song_tags = {tag.strip().lower() for tag in song_tags if tag.strip()}
    if desired_tags and song.get("mood_tags") is not None:
        matched_tags = desired_tags & song_tags
        tag_points = feature_weight * len(matched_tags) / len(desired_tags)
        score += tag_points
        reasons.append(f"mood tags match ({len(matched_tags)}/{len(desired_tags)}, +{tag_points:.2f})")

    preferred_decade = user_prefs.get("preferred_release_decade")
    if preferred_decade is not None and song.get("release_decade") is not None:
        decade_points = feature_weight if song["release_decade"] == preferred_decade else 0.0
        score += decade_points
        reasons.append(f"release decade match (+{decade_points:.2f})")

    for preference_key, feature_key, reason_label in (
        ("target_acousticness", "acousticness", "acousticness similarity"),
        ("target_danceability", "danceability", "danceability similarity"),
    ):
        target_value = user_prefs.get(preference_key)
        feature_value = song.get(feature_key)
        if target_value is not None and feature_value is not None:
            similarity = max(0.0, 1.0 - abs(float(feature_value) - float(target_value)))
            feature_points = feature_weight * similarity
            score += feature_points
            reasons.append(f"{reason_label} (+{feature_points:.2f})")

    return score, reasons


def score_song(
    user_prefs: Dict,
    song: Dict,
    mode: str = "balanced",
) -> Tuple[float, List[str]]:
    """Score a song using the selected core strategy and shared feature bonuses."""
    strategy = _get_scoring_strategy(mode)
    score, reasons = strategy.score_core(user_prefs, song)
    return _add_advanced_feature_scores(user_prefs, song, score, reasons)


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
) -> List[Tuple[Dict, float, str]]:
    """Return top-scoring songs with explanations and a repeat-artist penalty."""
    _get_scoring_strategy(mode)
    remaining = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        remaining.append((song, score, reasons))

    recommendations = []
    selected_artists = set()
    repeat_artist_penalty = 0.25

    while remaining and len(recommendations) < max(k, 0):
        best_index = max(
            range(len(remaining)),
            key=lambda index: remaining[index][1]
            - (repeat_artist_penalty if remaining[index][0]["artist"] in selected_artists else 0.0),
        )
        song, base_score, reasons = remaining.pop(best_index)
        penalty = repeat_artist_penalty if song["artist"] in selected_artists else 0.0
        final_score = base_score - penalty
        if penalty:
            reasons.append(f"repeat artist penalty (-{penalty:.2f})")
        explanation = "; ".join(reasons)
        recommendations.append((song, final_score, explanation))
        selected_artists.add(song["artist"])

    return recommendations
