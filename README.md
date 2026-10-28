# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Current music recommendation systems like Spotify, use information like listening history, likes, skips, playlists, and song characteristics to suggest music that users may enjoy. Some systems also use listening patterns from other users with similar tastes. 

Algorithm Recipe:
My recommender will compare each song with the user's preferences and calculate a relevance score. It will award 2.0 points for an exact genre match, 1.0 point for an exact mood match, and up to 1.0 point for energy similarity. Energy similarity is calculated by subtracting the absolute difference between the song's energy and the user's target energy from 1. The system will record reasons for each score, rank songs from highest to lowest, and return the top five recommendations.

Potential Bias:
Genre receives more points than mood, so songs in the preferred genre may rank higher even when other songs better match the user's mood and energy. The dataset is small and has an uneven distribution of genres, which may limit recommendation variety. The system also does not explicitly promote diversity in its results.

Each Song in my simulation will use the following features from the dataset:
- ID: A unique identifier for each song.
- Title: The name of the song.
- Artist: The artist who performs the song.
- Genre: The music category, such as pop, rock, lofi, or jazz.
- Mood: The song's mood, such as happy, chill, intense, or relaxed.
- Energy: A numerical value from 0.0 to 1.0 representing the song's energy.
- Tempo (BPM): The song's speed in beats per minute.
- Valence: A numerical feature representing how positive or happy the music sounds.
- Danceability: A numerical feature representing how suitable the music is for dancing.
- Acousticness: A numerical feature representing how acoustic the music sounds.

The UserProfile will contain:
- Favorite genre: The user's preferred music genre.
- Favorite mood: The mood the user wants to listen to.
- Target energy: The user's preferred energy level, from 0.0 to 1.0.



Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
python -m src.main
Loaded 18 songs.

Top 5 recommendations:

1. Sunrise City - Neon Echo
   Score: 3.98
   Why: genre match (+2.0); mood match(+1.0); energy similarity (+0.98)

2. Gym Hero - Max Pulse
   Score: 2.87
   Why: genre match (+2.0); energy similarity (+0.87)

3. Rooftop Lights - Indigo Parade
   Score: 1.96
   Why: mood match (+1.0); energy similarity (+0.96)

4. Saturday Static - The Brass Comets
   Score: 0.99
   Why: energy similarity (+0.99)

5. Paper Moon Fiesta - Luna Mar Azul
   Score: 0.97
   Why: energy similarity (+0.97)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



