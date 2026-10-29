# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
**GrooveHUB** 

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

GrooveHUB is designed to recommend songs based on a user's preferred genre, mood, and energy level. It is intended for classroom learning and demonstrating how a basic recommendation algorithm works. It assumes that users can describe their music preferences using these features. It is not designed to replace a real music streaming service or fully understand individual musical taste.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

GrooveHUB compares a user's preferences with each song's attributes. It awards 1 point for an exact genre match and 1 point for an exact mood match. Energy similarity can contribute up to 2 points and is calculated by subtracting the absolute difference between the song's energy and the user's target energy from 1, then multiplying the result by 2. 

The final score is calculated as:
Score = genre match + mood match + 2 × (1 − |song energy − target energy|)

The system adds these points together, sorts songs from highest to lowest score, and returns the top five recommendations. Each recommendation includes an explanation of the points it received. Compared with the original scoring approach, I reduced the genre weight from 2 points to 1 point and doubled the energy weight from a maximum of 1 point to 2 points.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The recommender uses a CSV catalog of 18 songs. Each song includes a title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The genres and moods cover different styles, but many genres appear only once, which limits the available choices. The scoring function currently uses only genre, mood, and energy. The dataset is small and cannot represent the full range of musical styles or personal preferences.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The recommender is simple to understand and explains why each song receives its score. It responds to different profiles by recommending Sunrise City for High-Energy Pop, Library Rain for Chill Lofi, and Storm Runner for Intense Rock. The scoring rules make it easy to test how changing feature weights affects the results. The system also provides a useful starting point for learning about ranking algorithms and personalized recommendations.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

My recommender uses genre, mood, and energy to calculate song scores. It does not use tempo, valence, danceability, or acousticness, even though these features are available in my dataset. This means it may miss important parts of a listener's musical taste. My dataset contains 18 songs. Lofi appears three times, pop appears twice, and most other genres appear only once. This limits the variety of recommendations available for many genres. The system also requires exact genre and mood matches, so it may not recognize similar styles or users who enjoy multiple genres. The scoring system does not penalize mismatches. A song can still rank highly because its energy matches the user's target, even if its genre or mood is different. My experiment doubled the energy weight, making energy similarity worth up to two points. This can cause high-energy songs to rank well for different profiles. The recommender could create a filter bubble by repeatedly favoring songs with similar energy or matching categories. However, my current tests show a risk of limited variety rather than proof of a full filter bubble. Adding more songs, using additional musical features, and introducing a diversity rule could improve the recommendations.
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested GrooveHUB using three user profiles: High-Energy Pop, Chill Lofi, and Intense Rock. I checked whether the top five recommendations matched each profile's preferred genre, mood, and energy level. The results were mostly reasonable. Sunrise City ranked first for High-Energy Pop, Library Rain ranked first for Chill Lofi, and Storm Runner ranked first for Intense Rock. Each leading song matched its profile's preferred genre and mood and had energy close to the target. One surprising result was that Gym Hero appeared in the High-Energy Pop recommendations even though its mood is intense rather than happy. It still ranked highly because it matched the preferred genre and had energy close to the target. Gym Hero also appeared in the Intense Rock recommendations because it matched the intense mood and had high energy, even though its genre is pop. Iron Orchard appeared in the recommendations based on energy similarity alone. These examples show that a song can earn a high score without matching every preference because the algorithm does not subtract points for mismatches.

Weight-Shift Experiment Results:
I changed the genre weight from 2 points to 1 point and doubled the energy similarity weight from a maximum of 1 point to 2 points. The mood weight remained at 1 point. I then reran the recommender for all three profiles. The top recommendation for each profile remained the same: Sunrise City for High-Energy Pop, Library Rain for Chill Lofi, and Storm Runner for Intense Rock. The rankings for High-Energy Pop and Intense Rock also stayed in the same order. The Chill Lofi rankings changed slightly. In the original results, Focus Flow ranked third and Spacewalk Thoughts ranked fourth. After the weight change, Spacewalk Thoughts moved to third place and Focus Flow moved to fourth. Spacewalk Thoughts matched the preferred mood and had energy close to the target, while Focus Flow matched the preferred genre but not the mood. Giving energy more weight allowed Spacewalk Thoughts to rank higher. This experiment showed that changing the importance of different features can change rankings even when the song catalog stays the same. However, the new rankings are not automatically more accurate. I would need to compare the recommendations with listeners' actual preferences to determine whether the changes improve their experience.

Profile Comparisons:
High-Energy Pop vs. Chill Lofi:
High-Energy Pop recommended Sunrise City first, while Chill Lofi recommended Library Rain first. Sunrise City matched the pop and happy preferences and had high energy. Library Rain matched the lofi and chill preferences and had energy close to the lower target. This makes sense because the profiles prefer different musical styles and energy levels. Some songs can still appear in both lists when their energy scores are high enough.

High-Energy Pop vs. Intense Rock:
High-Energy Pop recommended Sunrise City first, while Intense Rock recommended Storm Runner first. Both profiles also included Gym Hero, Storm Runner, and Iron Orchard in their top five. This makes sense because both profiles target high-energy music. However, the reasons for individual recommendations differ. Gym Hero earns genre and energy points for High-Energy Pop, but mood and energy points for Intense Rock. This illustrates how the same song can appeal to the scoring rules of different profiles for different reasons.

Chill Lofi vs. Intense Rock:
Chill Lofi recommended Library Rain first, while Intense Rock recommended Storm Runner first. Library Rain matched the lofi and chill preferences and had energy close to 0.3. Storm Runner matched the rock and intense preferences and had energy close to 0.95. These differences make sense because the profiles target different genres, moods, and energy levels. Some high-energy songs can still appear in the Intense Rock recommendations without matching the preferred genre or mood, because energy similarity contributes points independently.

Overall, the evaluations showed that GrooveHUB responds to different user preferences and that changing scoring weights can affect the rankings. The results also revealed limitations: energy can compensate for a genre or mood mismatch, and the system does not explicitly encourage variety.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

If I continued developing GrooveHUB, I would add tempo, danceability, and acousticness to the scoring system. I would also expand the song catalog to include more genres, moods, and artists. Finally, I would also add a diversity rule to reduce repetitive recommendations and help users discover different types of music.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

My biggest learning moment was discovering that changing the weights in a recommendation algorithm can change song rankings, even when the song data stays the same. I learned that a song can rank highly without matching every user preference because the algorithm adds points for the features it does match. AI tools helped me understand the scoring logic, review my code, and identify possible biases. However, I still needed to run the program and compare the actual results to make sure the explanations matched what happened. I was surprised that such a simple algorithm could produce recommendations that felt personalized. I also learned that reasonable-looking results do not mean the system fully understands someone's musical taste. If I continued this project, I would use more songs, include additional musical features in the scoring, and add a way to recommend a wider variety of music. I would also test more user profiles to see how well the system handles different or conflicting preferences.