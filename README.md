# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

GrooveHUB is a music recommender simulation that ranks songs based on a user's preferred genre, mood, and target energy level. It calculates a score for each song, explains why the song received its score, and returns the top five recommendations for each user profile. I experimented with changing the scoring weights to explore how the importance of genre, mood, and energy affects the recommendations. The project demonstrates how a simple recommendation algorithm works and how its design choices can influence its results.

---

## How The System Works

Current music recommendation systems like Spotify, use information like listening history, likes, skips, playlists, and song characteristics to suggest music that users may enjoy. Some systems also use listening patterns from other users with similar tastes. 

Initial Algorithm Recipe:
My recommender will compare each song with the user's preferences and calculate a relevance score. It will award 2.0 points for an exact genre match, 1.0 point for an exact mood match, and up to 1.0 point for energy similarity. Energy similarity is calculated by subtracting the absolute difference between the song's energy and the user's target energy from 1. The system will record reasons for each score, rank songs from highest to lowest, and return the top five recommendations.

Potential Bias:
Genre receives more points than mood, so songs in the preferred genre may rank higher even when other songs better match the user's mood and energy. The dataset is small and has an uneven distribution of genres, which may limit recommendation variety. The system also does not explicitly promote diversity in its results.

Updated Algorithm Recipe:
My recommender compares each song with the user's preferences and calculates a relevance score. It awards 1.0 point for an exact genre match, 1.0 point for an exact mood match, and up to 2.0 points for energy similarity. Energy similarity is calculated by subtracting the absolute difference between the song's energy and the user's target energy from 1, then multiplying the result by 2. The system records reasons for each score, ranks songs from highest to lowest, and returns the top five recommendations.

Bias:
Energy can contribute as much as the genre and mood matches combined, so songs with similar energy can rank highly even when their genre or mood is different. The dataset contains only 18 songs, and most genres appear only once, which limits variety. The system does not explicitly promote diversity or penalize mismatches. These limitations could lead to recommendations that do not fully reflect a user's preferences.

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
- Popularity: An illustrative score from 0 to 100.
- Release decade: An illustrative decade label, such as `1990s` or `2020s`.
- Mood tags: Multiple descriptive tags separated by `|` in the CSV.

The popularity, release-decade, mood-tag, acousticness, and danceability values in this small dataset are simulated for this project. They are not real-world measured or verified values.

The UserProfile will contain:
- Favorite genre: The user's preferred music genre.
- Favorite mood: The mood the user wants to listen to.
- Target energy: The user's preferred energy level, from 0.0 to 1.0.
- Optional preferences: `desired_mood_tags`, `preferred_release_decade`, `target_acousticness`, and `target_danceability` can further customize matches.



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
Initial Terminal Output:
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

Updated Terminal Output:
python -m src.main
Loaded 18 songs.

High-Energy Pop - Top 5 recommendations:

1. Sunrise City - Neon Echo
   Score: 3.84
   Why: genre match (+1.0); mood match (+1.0); energy similarity (+1.84)

2. Gym Hero - Max Pulse
   Score: 2.94
   Why: genre match (+1.0); energy similarity (+1.94)

3. Rooftop Lights - Indigo Parade
   Score: 2.72
   Why: mood match (+1.0); energy similarity (+1.72)

4. Storm Runner - Voltline
   Score: 1.98
   Why: energy similarity (+1.98)

5. Iron Orchard - Blackglass Harbor
   Score: 1.90
   Why: energy similarity (+1.90)

Chill Lofi - Top 5 recommendations:

1. Library Rain - Paper Lanterns
   Score: 3.90
   Why: genre match (+1.0); mood match (+1.0); energy similarity (+1.90)

2. Midnight Coding - LoRoom
   Score: 3.76
   Why: genre match (+1.0); mood match (+1.0); energy similarity (+1.76)

3. Spacewalk Thoughts - Orbit Bloom
   Score: 2.96
   Why: mood match (+1.0); energy similarity (+1.96)

4. Focus Flow - LoRoom
   Score: 2.80
   Why: genre match (+1.0); energy similarity (+1.80)

5. Field of Lanterns - Rowan Bell
   Score: 1.94
   Why: energy similarity (+1.94)

Intense Rock - Top 5 recommendations:

1. Storm Runner - Voltline
   Score: 3.92
   Why: genre match (+1.0); mood match (+1.0); energy similarity (+1.92)

2. Gym Hero - Max Pulse
   Score: 2.96
   Why: mood match (+1.0); energy similarity (+1.96)

3. Iron Orchard - Blackglass Harbor
   Score: 2.00
   Why: energy similarity (+2.00)

4. Sunrise City - Neon Echo
   Score: 1.74
   Why: energy similarity (+1.74)

5. Saturday Static - The Brass Comets
   Score: 1.72
   Why: energy similarity (+1.72)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

Profile Evaluation (Terminal Output):
python -m src.main
Loaded 18 songs.

High-Energy Pop - Top 5 recommendations:

1. Sunrise City - Neon Echo
   Score: 3.92
   Why: genre match (+2.0); mood match (+1.0); energy similarity (+0.92)

2. Gym Hero - Max Pulse
   Score: 2.97
   Why: genre match (+2.0); energy similarity (+0.97)

3. Rooftop Lights - Indigo Parade
   Score: 1.86
   Why: mood match (+1.0); energy similarity (+0.86)

4. Storm Runner - Voltline
   Score: 0.99
   Why: energy similarity (+0.99)

5. Iron Orchard - Blackglass Harbor
   Score: 0.95
   Why: energy similarity (+0.95)

Chill Lofi - Top 5 recommendations:

1. Library Rain - Paper Lanterns
   Score: 3.95
   Why: genre match (+2.0); mood match (+1.0); energy similarity (+0.95)

2. Midnight Coding - LoRoom
   Score: 3.88
   Why: genre match (+2.0); mood match (+1.0); energy similarity (+0.88)

3. Focus Flow - LoRoom
   Score: 2.90
   Why: genre match (+2.0); energy similarity (+0.90)

4. Spacewalk Thoughts - Orbit Bloom
   Score: 1.98
   Why: mood match (+1.0); energy similarity (+0.98)

5. Field of Lanterns - Rowan Bell
   Score: 0.97
   Why: energy similarity (+0.97)

Intense Rock - Top 5 recommendations:

1. Storm Runner - Voltline
   Score: 3.96
   Why: genre match (+2.0); mood match (+1.0); energy similarity (+0.96)

2. Gym Hero - Max Pulse
   Score: 1.98
   Why: mood match (+1.0); energy similarity (+0.98)

3. Iron Orchard - Blackglass Harbor
   Score: 1.00
   Why: energy similarity (+1.00)

4. Sunrise City - Neon Echo
   Score: 0.87
   Why: energy similarity (+0.87)

5. Saturday Static - The Brass Comets
   Score: 0.86
   Why: energy similarity (+0.86)


Initial Profile Evaluation:

I tested three profiles: High-Energy Pop, Chill Lofi, and Intense Rock. The results generally matched my expectations. High-Energy Pop ranked "Sunrise City" first, Chill Lofi ranked "Library Rain" first, and Intense Rock ranked "Storm Runner" first. The High-Energy Pop profile also ranked "Gym Hero" highly, even though its mood is intense rather than happy. This happens because genre is worth 2 points and energy similarity can contribute nearly another point. For Chill Lofi, "Library Rain" ranked above "Midnight Coding" because both songs match genre and mood, but "Library Rain" has energy closer to the target of 0.3. For Intense Rock, "Storm Runner" ranked first because it matches both genre and mood while having energy close to 0.95. These results show that the recommender responds to changes in user preferences, but a song can still rank highly without matching every preference. The algorithm uses fixed weights and does not explicitly promote variety.

Updated:
I changed the genre weight from 2 points to 1 point and doubled the energy similarity weight so that it could contribute up to 2 points. The mood weight remained at 1 point. I reran the recommender for High-Energy Pop, Chill Lofi, and Intense Rock. The top recommendation for each profile stayed the same: Sunrise City for High-Energy Pop, Library Rain for Chill Lofi, and Storm Runner for Intense Rock. However, the Chill Lofi ranking changed slightly. For the original weights, Focus Flow ranked third, and Spacewalk Thoughts ranked fourth. For the updated weights, Spacewalk Thoughts ranked third, and Focus Flow ranked fourth. Spacewalk Thoughts matches the preferred mood and has energy close to the target. Focus Flow matches the preferred genre but not the mood. Doubling the energy weight made Spacewalk Thoughts score higher. The experiment showed that changing the importance of different features can change rankings even when the song catalog stays the same. The updated results are consistent with the new scoring formula, but I cannot conclude that they are more accurate without comparing them with listeners' preferences.




---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

GrooveHUB uses a small catalog of only 18 songs, so it cannot represent the full range of musical tastes. It scores songs using genre, mood, and energy but does not use tempo, valence, danceability, or acousticness. Because the algorithm does not penalize mismatches, a song can rank highly even when it does not match the user's preferred mood or genre. Energy similarity can contribute up to two points, which may cause high-energy songs to appear in multiple profiles' recommendations. The system also lacks a diversity rule, so recommendations may become repetitive. These limitations mean that a high score does not necessarily guarantee that a listener will enjoy a song.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Working on GrooveHUB taught me that recommendation systems use scoring rules to rank items based on user preferences. I learned that changing the weights assigned to genre, mood, and energy can change the rankings even when the song catalog stays the same. I was surprised that songs such as Gym Hero could rank highly for different profiles because the algorithm rewards matching features without knocking mismatches. I also learned that a high recommendation score does not necessarily mean a listener will enjoy a song. A small dataset, unused musical features, and a lack of diversity rules can limit the quality of recommendations. Testing different profiles helped me understand why it is important to evaluate both the scoring formula and the actual results rather than assuming that an algorithm is accurate simply because it produces reasonable-looking rankings.


