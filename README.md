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

**Final chunk count:** 34 chunks across 10 sources (6 scraped successfully, 4 via manual fallback text)

## Sample Chunks

| # | Chunk ID | Source | Text (truncated) |
|---|----------|--------|-----------------|
| 1 | src_08_c00 | Patch NJ – Rutgers Menu Overhaul Article | Rutgers Ditches Cold Cuts, Chicken Nuggets In Menu Overhaul. Like chicken nuggets and cold cuts? They're no longer served at the Neilson main dining hall at Rutgers University's New Brunswick campus. Pork sausage is no longer offered at breakfast and hot sauce will no longer be served at wing night. Instead, smoked chicken sausage served with spinach on a whole-grain English muffin... |
| 2 | src_01_c02 | Rutgers Dining Services – Places to Eat | Every day, the scarlet red mobile truck serves gourmet medieval themed meals fresh off the grill. Rotating weekly schedule — Monday: Busch Campus, Tuesday: College Avenue Campus, Wednesday: Busch Campus, Thursday: Cook Campus, Friday: Livingston Campus... |
| 3 | src_01_c09 | Rutgers Dining Services – Places to Eat | The Starbucks Truck serves the entire menu from any other Starbucks location including sandwiches and pastries. RU Express is accepted. Monday: College Avenue by Alexander Library, Tuesday: Livingston by the towers, Wednesday: Cook by Biel Road... |
| 4 | src_10_c01 | r/rutgers – Top Dining Hall Threads | Henry's Diner on Livingston is so underrated. They have pancakes the size of your face and they accept meal swipes. Neilson has really good vegetarian options since they overhauled the menu. Livingston also has a solid salad bar... |
| 5 | src_01_c05 | Rutgers Dining Services – Places to Eat | Henry's Diner at the Plaza (Livingston) — enjoy a milkshake, customized burger or hearty breakfast. Hours: Monday–Friday 11:00am–6:00pm, meal swipes accepted at all times. Kilmer's Market offers hot and cold entrees, breakfast sandwiches, snacks, toiletries, and school supplies... |
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

## Retrieval Test Results

**Query 1: What are students' opinions about Livingston dining compared to the Atrium?**

| Rank | Source | Distance |
|------|--------|----------|
| 1 | Niche.com – Rutgers NB Campus Life Student Reviews | 0.3561 |
| 2 | Rutgers Dining Services – Places to Eat | 0.3604 |
| 3 | TikTok – Rutgers Livingston Dining Hall Tour | 0.3815 |
| 4 | r/rutgers – Top Dining Hall Threads | 0.3839 |
| 5 | Rutgers Dining Services – Places to Eat | 0.3973 |

Results 1, 3, and 4 are highly relevant — they are student review chunks that directly compare Livingston and the Atrium, mentioning the soft serve, Asian station, and 3-swipe cap. Result 2 is partially relevant, pulling in official dining info about food trucks rather than the comparison itself.

---

**Query 2: Does Rutgers have a Starbucks truck, and how does it work?**

| Rank | Source | Distance |
|------|--------|----------|
| 1 | Rutgers Dining Services – Places to Eat | 0.3195 |
| 2 | Rutgers Dining Services – Places to Eat | 0.3246 |
| 3 | Rutgers Dining Services – Places to Eat | 0.3247 |
| 4 | Rutgers Dining Services – Places to Eat | 0.3592 |
| 5 | Rutgers Dining Services – Places to Eat | 0.3789 |

Results 4 and 5 are directly relevant — they contain the exact Starbucks truck description, campus schedule, and meal swipe policy from the official dining page. Results 1–3 are partially relevant, covering other food trucks and meal swipe rules which share vocabulary with the query.

---

**Query 3: What can students with dietary restrictions eat at Neilson Dining Hall?**

| Rank | Source | Distance |
|------|--------|----------|
| 1 | Rutgers Dining Services – Places to Eat | 0.4118 |
| 2 | Rutgers Dining Services – Places to Eat | 0.4135 |
| 3 | Rutgers Dining Services – Places to Eat | 0.4416 |
| 4 | r/rutgers – Top Dining Hall Threads | 0.4620 |
| 5 | Patch NJ – Rutgers Menu Overhaul Article | 0.4717 |

Results 4 and 5 are relevant — they mention Neilson's vegetarian options and whole foods menu overhaul. Results 1–3 are off-target, pulling food truck chunks. This is the weakest retrieval of the three queries, with all distances above 0.41.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system prompt instructs the model to answer only from the provided documents, explicitly prohibiting use of general training knowledge. The exact instruction is: "Answer ONLY from the provided documents. Do not use your general training knowledge about Rutgers, dining halls, or New Brunswick restaurants. If the documents do not contain enough information to answer the question, say exactly: 'I don't have enough information on that in my sources.'" The model is also instructed to flag conflicts between official and student sources explicitly.

**How source attribution is surfaced in the response:**
Attribution is handled in two ways: the LLM is instructed to end every response with a "Sources:" section naming the documents it drew from, and source names are also collected programmatically from the retrieved chunks and displayed separately in the Gradio UI — so attribution is guaranteed even if the model forgets to cite.

## Example Responses

**Response 1 — Livingston vs Atrium (grounded, accurate):**

"According to student reviews, Livingston dining hall is highly praised and considered the best on campus. Students rave about the Mongolian grill, coconut milk ramen station, and soft serve ice cream. In contrast, the Atrium on College Ave is described as having average food quality and is limited by a 3 swipe per day limit, making it less desirable.

Sources:
- Niche.com – Rutgers NB Campus Life Student Reviews
- TikTok – Rutgers Livingston Dining Hall Tour
- r/rutgers – Top Dining Hall Threads"

---

**Response 2 — Starbucks truck (grounded, accurate):**

"Rutgers has a Starbucks Truck that makes its way around each campus throughout the week, serving the entire Starbucks menu including sandwiches and pastries. RU Express is accepted, and meal swipes are eligible per the retail policy.

Sources:
- Rutgers Dining Services – Places to Eat"

---

**Out-of-scope refusal — best pizza in Tokyo:**

"I don't have enough information on that in my sources. The provided documents only discuss dining options near Rutgers University in New Brunswick, New Jersey, and do not mention Tokyo or any pizza places in Tokyo.

Sources:
- Rutgers Student Centers – Places to Eat
- TripAdvisor – Best Restaurants Near Rutgers"

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are students' opinions about Livingston dining call compared to the Atrium on College Avenue ? | Livingston is generally considered the best dining hall as students mention the salad bar, Asian station, and great soft-serve ice cream. The Atrium gets mixed reviews and is mainly liked for the option of food takeaway and eating it anywhere you like. | Livingston praised for Mongolian grill, ramen, soft serve. Atrium described as average and worst due to 3-swipe limit. | Relevant  | Accurate | 
| 2 | Can I use my meal swipe in the Busch student center? | No, because the restaurants in the center only accept Rutgers express cards, not standard meal swipes. | System said it didn't have enough information, only found Busch Dining Hall which does accept swipes. | Partially relevant | Partially accurate| 
| 3 | What are some budget friendly places to eat near College Avenue? | Students recommend Daniel's Pizza for cheap slices, Sakana for all-you-can-eat sushi, and Old Man Rafferty's for American comfort food. | Named Gerlanda's Pizza, Szechwan Ichiban, Panera — no student budget framing, acknowledged budget info wasn't explicit. | Partially relevant | Partially accurate | 
| 4 | Does Rutgers have a Starbucks truck, and how does it work? | Yes, there's a Starbucks truck that goes across the different campuses throughout the week and accepts standars meal swipes. It serves the full menu including food. | Correct — confirmed truck exists, full Starbucks menu, RU Express and meal swipes accepted, rotates campuses. | Relevant  | Accurate | 
| 5 | What can students with dietary restrictions eat at Neilson Dining Hall? | Neilson has gluten-free and vegetarian options, a salad bar, and has moved away from processed foods toward whole ingredients like roasted meats. | Mentioned vegetarian options and new whole foods menu items like purple Peruvian hash. Partial but grounded. | Partially relevant | Partially accurate | 

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
Q2 — Can I use my meal swipe in the Busch student center?

**What the system returned:**
The system said it didn't have enough information, noting only that Busch Dining Hall accepts meal swipes. It did not correctly answer that the Busch Student Center restaurants only accept RU Express, not standard meal swipes.

**Root cause (tied to a specific pipeline stage):**
This is a retrieval stage failure caused by terminology mismatch. The query uses "Busch student center" but the relevant chunk from src_03 (Rutgers Student Centers – Places to Eat) describes swipe rules using different phrasing. The all-MiniLM-L6-v2 embedding model did not surface src_03 as a top result because "student center" and "Busch" didn't co-occur strongly enough in any single chunk to match the query embedding. The relevant policy information was present in the corpus but wasn't retrieved.

**What you would change to fix it:**
Attach campus name and location type as metadata filters so queries mentioning "Busch student center" can explicitly filter for src_03 chunks. Alternatively, expanding the fallback text for src_03 with more explicit phrasing like "Busch Student Center does not accept meal swipes" would make the semantic match stronger.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The planning.md chunking strategy (200–300 tokens, 30-token overlap, paragraph-aware splitting) directly shaped the chunk_text() implementation. Having the chunk size decided before writing any code prevented the common mistake of using a single large chunk per document, which would have made retrieval too coarse to distinguish between individual dining halls.

**One way your implementation diverged from the spec, and why:**
The spec planned to use the Claude API for generation (Milestone 5), but the implementation switched to Groq's llama-3.3-70b-versatile. This change was made because Groq provides a free tier with no usage cost, making it more practical for a student project. The switch required no changes to the retrieval or chunking pipeline — only the API client and model name changed.

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

- *What I gave the AI: My planning.md chunking strategy section and pipeline diagram, asking it to implement fetch_and_clean() and chunk_text().
- *What it produced: A complete pipeline.py with trafilatura-based scraping, paragraph-aware chunking, and a FALLBACK_TEXTS dict for blocked sources.
- *What I changed or overrode: Added manual fallback text for src_05, src_06, src_07, and src_10 after those sources returned 403 errors or sparse extractions. Also corrected a syntax error caused by unescaped quotes in the fallback text.

**Instance 2**

- *What I gave the AI: My retrieval approach section (all-MiniLM-L6-v2, top-k=5, ChromaDB) and the 3 evaluation questions, asking it to implement build_index() and retrieve() and run a retrieval test.
- *What it produced: retrieve.py with ChromaDB persistent storage, cosine distance scoring, and a test function that printed distance scores and flagged weak matches above 0.5.
- *What I changed or overrode: Switched the generation backend from Claude API to Groq after reviewing the Milestone 5 instructions, which recommended Groq as the free-tier default.

---

## Query Interface

The system uses a Gradio web UI accessible at http://localhost:7860.

**Input:** A plain text question typed into the "Your question" field. 
Five example questions are provided as clickable buttons on the right side.

**Output:** Two fields — "Answer" displays the grounded response with a 
Sources section at the bottom listing which documents were used. 
"Retrieved from" displays the programmatically collected source names 
as a separate list, guaranteed regardless of LLM output.

**Sample interaction:**

Input: "Does Rutgers have a Starbucks truck, and how does it work?"

Answer: "Rutgers has a Starbucks Truck that makes its way around each 
campus throughout the week, serving the entire menu from any other 
Starbucks location, including sandwiches and pastries. RU Express is 
accepted, and meal swipes are eligible per the retail policy. The truck 
rotates campuses on a weekly schedule — Monday on College Avenue, 
Tuesday on Livingston, Wednesday on Cook, Thursday on Busch, and 
Friday on George Street.

Sources:
- Rutgers Dining Services – Places to Eat"

Retrieved from:
- Rutgers Dining Services – Places to Eat"