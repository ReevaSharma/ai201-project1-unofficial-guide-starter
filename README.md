# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

     Domain: Campus dining and food spots for Rutgers University–New Brunswick students.

     Rutgers' official dining site gives the locations and hours but gives no student opinions, honest comparisons, or practical tips and it won't tell you that Livingston Dining Commons is widely considered the best hall, that the Atrium on College Ave has a 3-swipe daily cap, or that Henry's Diner on Livingston accepts meal swipes and has pancakes the size of dinner plates. That insider knowledge is scattered across Reddit threads, student blogs, Niche reviews, TikTok, and word of mouth. 
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rutgers Dining Services – Places to Eat | Official list of every on-campus dining location with meal plan eligibility notes | https://food.rutgers.edu/places-eat |
| 2 |Rutgers NB Student Housing & Dining Overview | University overview of dining across all five campuses; mentions HARVEST café and RU Express | https://newbrunswick.rutgers.edu/student-experience/student-housing-dining |
| 3 | Rutgers Student Centers – Places to Eat | Details on Atrium (College Ave), Café West, and swipe rules at retail locations | https://sca.rutgers.edu/student-centers/places-eat |
| 4 | Rutgers Libraries – Grad Dining & Entertainment Guide | Curated list of off-campus restaurants in New Brunswick: Indochine, Ramen Nagomi, Dashen, Harvest Moon, Stuff Yer Face | https://libguides.rutgers.edu/nbgrad/dining |
| 5 | Niche.com – Rutgers NB Campus Life Student Reviews | Aggregated short student reviews mentioning dining hall quality, Atrium complaints, Livingston praise | https://www.niche.com/colleges/rutgers-universitynew-brunswick/campus-life/ |
| 6 | TikTok – Rutgers Livingston Dining Hall Tour | Student tour of Livingston Dining Commons: Mongolian station, coconut milk ramen callouts | https://www.tiktok.com/discover/rutgers-livingston-dining-hall |
| 7 | TripAdvisor – Best Restaurants Near Rutgers | Student and visitor reviews of downtown New Brunswick restaurants within walking distance of campus | https://www.tripadvisor.com/RestaurantsNear-g46664-d7841029-Rutgers_University-New_Brunswick_New_Jersey.html |
| 8 | Patch NJ – Rutgers Menu Overhaul Article | Coverage of Rutgers switching to whole foods, roasted meats in-house; context on Neilson menu philosophy | https://patch.com/new-jersey/newbrunswick/cold-cuts-chicken-nuggets-way-out-rutgers-university |
| 9 | CampusReel – Rutgers Dining Hall Video Reviews | Student-written summaries and video descriptions of Busch, Livingston, and Cook/Doug dining | https://www.campusreel.org/colleges/rutgers-university-new-brunswick/dining_food |
| 10 | r/rutgers (reddit thread) – Top dining hall threads | Student forum | https://www.reddit.com/r/rutgers/search/?q=dining+hall&sort=top |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 200-300 tokens (200-300 words)

**Overlap:** 30 tokens (20 words)

**Why these choices fit your documents:** The sources are short: official dining entries run 40–60 tokens after stripping boilerplate, Patch paragraphs 50–80, Reddit tips and TikTok summaries 1–3 sentences. A 200–300 token chunk fits one complete location entry or review without bundling unrelated halls together. Overlap is kept to 30 tokens — on 60-token entries, anything larger causes near-total duplication between chunks. CampusReel (source 9) and TripAdvisor (source 7) may yield longer passages and will be split at paragraph boundaries and capped at 300 tokens.

**Final chunk count:** ******----*****

---

## Embedding Model


<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** 
all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
I'm using all-MiniLM-L6-v2 because it seemed like the standard starting point for a project like this — it's fast, runs locally, and works well on short text like reviews. If I were building this for real users, I'd probably want to think about a few things I learned along the way: the model has a 256-token input limit, which means longer chunks could get silently cut off (a bigger model like all-mpnet-base-v2 would handle that better); it's not trained on college student slang, so a query like "is the atrium mid" might not match the right chunks the way a human would expect; and since Rutgers has a lot of international students, a multilingual model could make the guide more accessible. For now, top-k of 5 felt like a reasonable guess — enough chunks to answer a multi-part question without overwhelming the LLM with irrelevant context.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are students' opinions about Livingsto dining call compared to the Atrium on College Avenue ? | Livingston is generally considered the best dining hall as students mention the salad bar, Asian station, and great soft-serve ice cream. The Atrium gets mixed reviews and is mainly liked for the option of food takeaway and eating it anywhere you like. | | | |
| 2 | Can I use my meal swipe in the Busch student center? | No, because the restaurants in the center only accept Rutgers express cards, not standard meal swipes. | | | |
| 3 | What are some student friendly budget places to eat near College Avenue? | Students recommend Daniel's Pizza for cheap slices, Sakana for all-you-can-eat sushi, and Old Man Rafferty's for American comfort food. | | | |
| 4 | Does Rutgers have a Starbucks truck, and how does it work? | Yes, there's a Starbucks truck that goes across the different campuses throughout the week and accepts standars meal swipes. It serves the full menu including food. | | | |
| 5 | What can students with dietary restrictions eat at Neilson Dining Hall? | Neilson has gluten-free and vegetarian options, a salad bar, and has moved away from processed foods toward whole ingredients like roasted meats. | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
