import re
from pathlib import Path
import pytest

from src.main import format_recommendations_table
from src.recommender import Song, UserProfile, Recommender, load_songs, recommend_songs, score_song

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_recommend_songs_penalizes_repeat_artists_when_alternatives_exist():
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }
    songs = [
        {"title": "Top", "artist": "Artist A", "genre": "pop", "mood": "happy", "energy": 0.8},
        {"title": "Near Top", "artist": "Artist A", "genre": "pop", "mood": "happy", "energy": 0.75},
        {"title": "Alternative", "artist": "Artist B", "genre": "pop", "mood": "happy", "energy": 0.72},
    ]

    results = recommend_songs(user_prefs, songs, k=3)

    assert len(results) == 3
    assert [song["title"] for song, _, _ in results] == ["Top", "Alternative", "Near Top"]
    assert results[0][1] == 4.0
    assert "genre match (+1.0)" in results[0][2]
    assert "mood match (+1.0)" in results[0][2]
    assert abs(results[2][1] - 3.65) < 1e-9
    assert "repeat artist penalty (-0.25)" in results[2][2]


def test_csv_advanced_features_are_valid_for_all_songs():
    csv_path = Path(__file__).parents[1] / "data" / "songs.csv"
    songs = load_songs(str(csv_path))

    assert len(songs) == 18
    for song in songs:
        assert 0 <= song["popularity"] <= 100
        assert re.fullmatch(r"\d{4}s", song["release_decade"])
        assert song["mood_tags"]
        assert 0.0 <= song["acousticness"] <= 1.0
        assert 0.0 <= song["danceability"] <= 1.0


def test_score_song_optional_advanced_preferences_are_bounded_and_explained():
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "popularity": 80,
        "release_decade": "2020s",
        "mood_tags": ["euphoric", "uplifting"],
        "acousticness": 0.7,
        "danceability": 0.6,
    }
    prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "desired_mood_tags": ["euphoric", "relaxed"],
        "preferred_release_decade": "2020s",
        "target_acousticness": 0.7,
        "target_danceability": 0.9,
    }

    score, reasons = score_song(prefs, song)

    assert abs(score - 5.0) < 1e-9
    assert any("popularity prior (+0.20)" in reason for reason in reasons)
    assert any("mood tags match (1/2, +0.12)" in reason for reason in reasons)
    assert any("release decade match (+0.25)" in reason for reason in reasons)
    assert any("acousticness similarity (+0.25)" in reason for reason in reasons)
    assert any("danceability similarity (+0.17)" in reason for reason in reasons)


def test_score_song_works_when_optional_preferences_and_features_are_omitted():
    prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }
    song = {"genre": "pop", "mood": "happy", "energy": 0.8}

    score, reasons = score_song(prefs, song)

    assert score == 4.0
    assert len(reasons) == 3


def test_scoring_modes_use_distinct_core_weights_and_share_advanced_bonuses():
    prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
    }
    song = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.7,
        "popularity": 80,
        "release_decade": "2020s",
        "mood_tags": ["uplifting"],
        "acousticness": 0.4,
        "danceability": 0.8,
    }
    prefs.update(
        desired_mood_tags=["uplifting"],
        preferred_release_decade="2020s",
        target_acousticness=0.4,
        target_danceability=0.8,
    )

    balanced_score, balanced_reasons = score_song(prefs, song)
    genre_score, genre_reasons = score_song(prefs, song, mode="genre-first")
    energy_score, energy_reasons = score_song(prefs, song, mode="energy-focused")

    assert score_song(prefs, song, mode="balanced") == (balanced_score, balanced_reasons)
    assert "genre match (+2.0)" in genre_reasons
    assert "mood match (+0.5)" in genre_reasons
    assert "energy similarity (+0.80)" in genre_reasons
    assert "genre match (+0.5)" in energy_reasons
    assert "mood match (+0.5)" in energy_reasons
    assert "energy similarity (+2.40)" in energy_reasons
    assert energy_score != balanced_score
    for reason in (
        "popularity prior",
        "mood tags match",
        "release decade match",
        "acousticness similarity",
        "danceability similarity",
    ):
        assert any(reason in item for item in genre_reasons)
        assert any(reason in item for item in energy_reasons)


def test_recommend_songs_rejects_unknown_mode():
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }
    with pytest.raises(ValueError, match="Unknown scoring mode"):
        recommend_songs(user_prefs, [], mode="experimental")


def test_diversity_penalty_applies_in_every_scoring_mode():
    prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }
    songs = [
        {"title": "First", "artist": "Artist A", "genre": "pop", "mood": "happy", "energy": 0.8},
        {"title": "Repeat", "artist": "Artist A", "genre": "pop", "mood": "happy", "energy": 0.75},
        {"title": "Alternative", "artist": "Artist B", "genre": "pop", "mood": "happy", "energy": 0.72},
    ]

    for mode in ("balanced", "genre-first", "energy-focused"):
        results = recommend_songs(prefs, songs, k=3, mode=mode)
        assert results[1][0]["artist"] == "Artist B"
        repeated_result = next(result for result in results if result[0]["title"] == "Repeat")
        assert "repeat artist penalty (-0.25)" in repeated_result[2]


def test_recommendation_table_wraps_long_text_and_keeps_all_reasons():
    recommendations = [
        (
            {
                "title": "A Very Long Imaginary Song Title That Needs Wrapping",
                "artist": "An Artist Name That Is Also Quite Long",
            },
            4.27,
            "genre match (+1.0); mood match (+1.0); energy similarity (+1.84); "
            "popularity prior (+0.20); repeat artist penalty (-0.25)",
        )
    ]

    table = format_recommendations_table(recommendations)
    rows = table.splitlines()

    assert "Rank" in table and "Song" in table and "Artist" in table
    assert "Score" in table and "Reasons" in table
    assert all(len(row) < 80 for row in rows)
    assert "Very" in table and "Imaginary" in table
    assert "genre match (+1.0)" in table
    assert "mood match (+1.0)" in table
    assert "energy similarity (+1.84)" in table
    assert "popularity prior (+0.20)" in table
    assert "repeat artist penalty (-0.25)" in table
    assert "4.27" in table
