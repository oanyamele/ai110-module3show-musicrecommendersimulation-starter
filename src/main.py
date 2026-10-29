"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

from .recommender import load_songs, recommend_songs

SCORING_MODE = "balanced"


def format_recommendations_table(recommendations: list) -> str:
    """Format ranked recommendations as a wrapped ASCII table."""
    headers = ("Rank", "Song", "Artist", "Score", "Reasons")
    widths = (4, 13, 10, 6, 30)
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def format_row(values: tuple, is_header: bool = False) -> list[str]:
        wrapped_cells = []
        for column_index, (value, width) in enumerate(zip(values, widths)):
            cell_text = str(value).replace("\n", " ")
            if column_index == len(widths) - 1 and not is_header:
                reasons = [reason.strip() for reason in cell_text.split(";")]
                wrapped = [
                    line
                    for reason in reasons
                    for line in (textwrap.wrap(reason, width=width) or [""])
                ]
            else:
                wrapped = textwrap.wrap(cell_text, width=width) or [""]
            wrapped_cells.append(wrapped)
        lines = []
        for line_index in range(max(len(cell) for cell in wrapped_cells)):
            cells = [
                cell[line_index] if line_index < len(cell) else ""
                for cell in wrapped_cells
            ]
            lines.append("| " + " | ".join(
                cell.ljust(width) for cell, width in zip(cells, widths)
            ) + " |")
        return lines

    table_lines = [border, *format_row(headers, is_header=True), border]
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        table_lines.extend(format_row((rank, song["title"], song["artist"], f"{score:.2f}", explanation)))
        table_lines.append(border)
    return "\n".join(table_lines)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.")
    print(f"Scoring mode: {SCORING_MODE}")

    profiles = [
        (
            "High-Energy Pop",
            {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.9},
        ),
        (
            "Chill Lofi",
            {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.3},
        ),
        (
            "Intense Rock",
            {"favorite_genre": "rock", "favorite_mood": "intense", "target_energy": 0.95},
        ),
    ]

    for profile_name, user_prefs in profiles:
        recommendations = recommend_songs(
            user_prefs,
            songs,
            k=5,
            mode=SCORING_MODE,
        )
        print(f"\n{profile_name} - Top 5 recommendations:")
        print(format_recommendations_table(recommendations))


if __name__ == "__main__":
    main()
