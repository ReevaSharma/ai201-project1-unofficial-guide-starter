# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Domain: Campus dining and food spots for Rutgers University–New Brunswick students.

Rutgers' official dining site gives the locations and hours but gives no student opinions, honest comparisons, or practical tips and it won't tell you that Livingston Dining Commons is widely considered the best hall, that the Atrium on College Ave has a 3-swipe daily cap, or that Henry's Diner on Livingston accepts meal swipes and has pancakes the size of dinner plates. That insider knowledge is scattered across Reddit threads, student blogs, Niche reviews, TikTok, and word of mouth. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 200-300 tokens (200-300 words)

**Overlap:** 30 tokens (20 words)

**Reasoning:**

The sources are short: official dining entries run 40–60 tokens after stripping boilerplate, Patch paragraphs 50–80, Reddit tips and TikTok summaries 1–3 sentences. A 200–300 token chunk fits one complete location entry or review without bundling unrelated halls together. Overlap is kept to 30 tokens — on 60-token entries, anything larger causes near-total duplication between chunks. CampusReel (source 9) and TripAdvisor (source 7) may yield longer passages and will be split at paragraph boundaries and capped at 300 tokens.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** 
all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 
5

**Production tradeoff reflection:**
I'm using all-MiniLM-L6-v2 because it seemed like the standard starting point for a project like this — it's fast, runs locally, and works well on short text like reviews. If I were building this for real users, I'd probably want to think about a few things I learned along the way: the model has a 256-token input limit, which means longer chunks could get silently cut off (a bigger model like all-mpnet-base-v2 would handle that better); it's not trained on college student slang, so a query like "is the atrium mid" might not match the right chunks the way a human would expect; and since Rutgers has a lot of international students, a multilingual model could make the guide more accessible. For now, top-k of 5 felt like a reasonable guess — enough chunks to answer a multi-part question without overwhelming the LLM with irrelevant context.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are students' opinions about Livingsto dining call compared to the Atrium on College Avenue ? | Livingston is generally considered the best dining hall as students mention the salad bar, Asian station, and great soft-serve ice cream. The Atrium gets mixed reviews and is mainly liked for the option of food takeaway and eating it anywhere you like. |
| 2 | Can I use my meal swipe in the Busch student center? | No, because the restaurants in the center only accept Rutgers express cards, not standard meal swipes. |
| 3 | What are some student friendly budget places to eat near College Avenue? | Students recommend Daniel's Pizza for cheap slices, Sakana for all-you-can-eat sushi, and Old Man Rafferty's for American comfort food. |
| 4 | Does Rutgers have a Starbucks truck, and how does it work? | Yes, there's a Starbucks truck that goes across the different campuses throughout the week and accepts standars meal swipes. It serves the full menu including food.
| 5 | What can students with dietary restrictions eat at Neilson Dining Hall? | Neilson has gluten-free and vegetarian options, a salad bar, and has moved away from processed foods toward whole ingredients like roasted meats. | 

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Vague reviews may cause off topic chunks. A lot of student opinions don't name a specific hall, so a query about the salad bar could pull chunks from Livingston, Neilson, and somewhere unrelated. I'm planning to attach hall name and campus as metadata to each chunk so I can filter before searching.

2. Official sources and students often go against each other. The Atrium is described as "modern and innovative" on the official site but students call it underwhelming. I'll try to handle this in the system prompt by telling the LLM to prefer student sources for opinions and official sources for facts like hours and meal plan rules. 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

     Ingestion: requests, trafilatura ---> Chunking: Python libraries ---> Embedding + Vector Store: all-MiniLM-L6-v2 (sentence-transformers), chromadb ---> Retrieval: chromadb ---> Generation: claude API (anthropic) 

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
Claude --> I will ask the model to implement two functions: fetch_and_clean(url) -> str (using trafilatura to strip nav/boilerplate) and chunk_text(text, chunk_size=350, overlap=50) -> list[dict] using tiktoken to count tokens for the 10 URLs (1) each chunk dict has the required keys text, source id, source name, chunk id, (2) no chunk exceeds 400 tokens when measured with tiktoken, and (3) consecutive chunks share the expected 50-token overlap when I diffrentiate them manually on two test documents.

**Milestone 4 — Embedding and retrieval:**
Claude --> I will ask it to implement build_index(chunks: list[dict]) using sentence-transformers + ChromaDB, and retrieve(query: str, k=5) -> list[dict]. I'll verify by running all 5 evaluation questions through retrieve() before any generation, inspecting the raw returned chunks to confirm they're topically relevant — e.g., a query about Livingston should return chunks that mention Livingston, not only Busch or Neilson.

**Milestone 5 — Generation and interface:**
Claude --> I'll give Claude the Evaluation Report table and ask it to implement generate_answer(query: str, chunks: list[dict]) -> str using the its API, with a system prompt instructing the model to answer as a Rutgers student guide, cite source names in its response, and flag conflicts between official and student sources. I'll verify each of the 5 evaluation questions by comparing the generated answer against the expected answers.