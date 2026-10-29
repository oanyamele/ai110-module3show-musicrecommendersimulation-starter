# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**
I used an AI coding assistant to extend GrooveHUB with advanced song features, artist diversity, multiple scoring modes, and formatted terminal output.

**Prompts used:**
- Challenge 1 — "Add at least five advanced song attributes, update the scoring logic, document simulated data, and add tests."
- Challenge 2 — "Implement Balanced, Genre-First, and Energy-Focused modes using a modular design pattern. Add a mode selector and tests."
- Challenge 3 — "Apply a 0.25-point penalty to songs by already-recommended artists. Update explanations and add tests."
- Challenge 4 — "Display recommendations in an ASCII table showing rank, song, artist, score, and scoring reasons. Handle long text and add tests."

**What did the agent generate or change?**
- data/songs.csv: Added popularity, release decade, and mood tags.
- src/recommender.py: Added advanced-feature scoring, three scoring strategies, and an artist-diversity penalty.
- src/main.py: Added scoring-mode selection and formatted recommendation tables.
- tests/test_recommender.py: Added tests for scoring, diversity, strategies, and table formatting.
- README.md: Documented the additional features.


**What did you verify or fix manually?**
I ran the application in all three scoring modes and compared the recommendations. I checked that the diversity penalty appeared in explanations, advanced features contributed to scores, and the table displayed all reasons. I also reviewed and reran tests after the AI corrected issues with score formatting, invalid modes, and table width.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**
Strategy

**How did AI help you brainstorm or implement it?**
The AI suggested separate scoring strategies while keeping advanced-feature scoring and artist-diversity logic shared. It also recommended a configurable SCORING_MODE setting in main.py.

**How does the pattern appear in your final code?**
In src/recommender.py, Balanced, Genre-First, and Energy-Focused strategies use different genre, mood, and energy weights. In src/main.py, SCORING_MODE selects the strategy. I tested all three modes and confirmed that their scores and explanations reflected the selected weights.
