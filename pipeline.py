"""
Milestone 3 — Document Ingestion, Cleaning, and Chunking
Rutgers Dining Unofficial Guide RAG Pipeline

Stages:
  1. fetch_and_clean(url) -> str       — scrape + strip boilerplate via trafilatura
  2. chunk_text(text, ...) -> list     — token-aware chunking with overlap via tiktoken
  3. build_corpus(sources) -> list     — runs both stages across all 10 sources
  4. inspect_chunks(chunks)            — prints 5 random chunks for manual review
"""

import re
import random
import json
import time
from typing import Optional

# ---------------------------------------------------------------------------
# Dependencies (install with):
#   pip install trafilatura tiktoken requests
# ---------------------------------------------------------------------------

try:
    import trafilatura
    from trafilatura.settings import use_config
except ImportError:
    raise ImportError("Run: pip install trafilatura")

try:
    import tiktoken
except ImportError:
    raise ImportError("Run: pip install tiktoken")

try:
    import requests
except ImportError:
    raise ImportError("Run: pip install requests")


# ---------------------------------------------------------------------------
# SOURCES  (mirrors your planning.md table)
# ---------------------------------------------------------------------------

SOURCES = [
    {
        "id": "src_01",
        "name": "Rutgers Dining Services – Places to Eat",
        "url": "https://food.rutgers.edu/places-eat",
        "type": "official",
    },
    {
        "id": "src_02",
        "name": "Rutgers NB Student Housing & Dining Overview",
        "url": "https://newbrunswick.rutgers.edu/student-experience/student-housing-dining",
        "type": "official",
    },
    {
        "id": "src_03",
        "name": "Rutgers Student Centers – Places to Eat",
        "url": "https://sca.rutgers.edu/student-centers/places-eat",
        "type": "official",
    },
    {
        "id": "src_04",
        "name": "Rutgers Libraries – Grad Dining & Entertainment Guide",
        "url": "https://libguides.rutgers.edu/nbgrad/dining",
        "type": "curated",
    },
    {
        "id": "src_05",
        "name": "Niche.com – Rutgers NB Campus Life Student Reviews",
        "url": "https://www.niche.com/colleges/rutgers-universitynew-brunswick/campus-life/",
        "type": "student_review",
    },
    {
        "id": "src_06",
        "name": "TikTok – Rutgers Livingston Dining Hall Tour",
        "url": "https://www.tiktok.com/discover/rutgers-livingston-dining-hall",
        "type": "student_review",
    },
    {
        "id": "src_07",
        "name": "TripAdvisor – Best Restaurants Near Rutgers",
        "url": "https://www.tripadvisor.com/RestaurantsNear-g46664-d7841029-Rutgers_University-New_Brunswick_New_Jersey.html",
        "type": "review",
    },
    {
        "id": "src_08",
        "name": "Patch NJ – Rutgers Menu Overhaul Article",
        "url": "https://patch.com/new-jersey/newbrunswick/cold-cuts-chicken-nuggets-way-out-rutgers-university",
        "type": "news",
    },
    {
        "id": "src_09",
        "name": "CampusReel – Rutgers Dining Hall Video Reviews",
        "url": "https://www.campusreel.org/colleges/rutgers-university-new-brunswick/dining_food",
        "type": "student_review",
    },
    {
        "id": "src_10",
        "name": "r/rutgers – Top Dining Hall Threads",
        "url": "https://www.reddit.com/r/rutgers/search/?q=dining+hall&sort=top",
        "type": "student_review",
    },
]


# ---------------------------------------------------------------------------
# STAGE 1 — FETCH AND CLEAN
# ---------------------------------------------------------------------------

# trafilatura config: be strict about boilerplate removal
_traf_config = use_config()
_traf_config.set("DEFAULT", "EXTRACTION_TIMEOUT", "30")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; RutgersDiningBot/1.0; "
        "+https://github.com/student/rutgers-dining-guide)"
    )
}


def _post_clean(text: str) -> str:
    """
    Secondary cleaning pass after trafilatura.
    Removes leftover HTML entities, excessive whitespace, and
    common nav/footer fragments that trafilatura sometimes misses.
    """
    # Decode common HTML entities
    replacements = {
        "&amp;": "&", "&nbsp;": " ", "&lt;": "<", "&gt;": ">",
        "&quot;": '"', "&#39;": "'", "&mdash;": "—", "&ndash;": "–",
        "&rsquo;": "'", "&lsquo;": "'", "&rdquo;": '"', "&ldquo;": '"',
    }
    for entity, char in replacements.items():
        text = text.replace(entity, char)

    # Strip any remaining HTML tags (safety net)
    text = re.sub(r"<[^>]+>", "", text)

    # Collapse 3+ newlines → 2 (preserve paragraph breaks)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip lines that look like nav/UI artifacts (very short, no sentence structure)
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Skip lines that are just a word or two and look like nav items
        if len(stripped) < 5 and stripped not in ("", "\n"):
            continue
        cleaned_lines.append(line)
    text = "\n".join(cleaned_lines)

    # Normalize whitespace within lines (multiple spaces → one)
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text.strip()


def fetch_and_clean(url: str, source_id: str = "", retries: int = 2) -> Optional[str]:
    """
    Fetch a URL and extract main content text using trafilatura.
    Falls back to a simple requests + trafilatura pipeline.

    Returns cleaned text string, or None if fetch fails.

    NOTE: Some sources (TikTok, Niche, Reddit) block scrapers or require
    JavaScript rendering. For those, replace with manually saved .txt files
    (see FALLBACK_TEXTS dict below) and this function will return the local copy.
    """
    # Check for manually saved fallback first
    if source_id in FALLBACK_TEXTS:
        print(f"  [FALLBACK] Using saved text for {source_id}")
        return _post_clean(FALLBACK_TEXTS[source_id])

    for attempt in range(retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()

            # trafilatura's main extraction
            raw = response.text
            extracted = trafilatura.extract(
                raw,
                config=_traf_config,
                include_comments=False,   # skip comment sections
                include_tables=True,      # keep dining hall comparison tables
                no_fallback=False,        # use fallback extractor if main fails
                favor_precision=True,     # prefer less text but more accurate
            )

            if not extracted or len(extracted.strip()) < 50:
                print(f"  [WARN] Sparse extraction for {source_id} ({url}) — may need fallback text")
                return None

            return _post_clean(extracted)

        except requests.exceptions.HTTPError as e:
            print(f"  [HTTP {e.response.status_code}] {source_id}: {url}")
            return None
        except Exception as e:
            if attempt < retries:
                time.sleep(2 ** attempt)  # exponential backoff
                continue
            print(f"  [ERROR] {source_id} after {retries} retries: {e}")
            return None


# ---------------------------------------------------------------------------
# FALLBACK TEXTS
# ---------------------------------------------------------------------------
# For sources that block scrapers (TikTok, Reddit, Niche), paste the raw
# text you copied manually here. Use the source id as the key.
# Example:
#   "src_05": """Niche review text pasted here..."""
#
# This keeps the pipeline consistent — fetch_and_clean() checks this dict
# before hitting the network, so you never need to change the call sites.

FALLBACK_TEXTS: dict[str, str] = {
    "src_05": """Rutgers dining is honestly pretty good compared to other schools. Livingston dining hall is the best one on campus by far. The food variety is great, they have an Asian station, a salad bar, and the soft serve ice cream is amazing. The Atrium on College Ave is convenient but the food quality is just average. There is a 3 swipe per day limit at the Atrium which is really annoying if you live on College Ave. Cook and Douglass dining is underrated, the food is solid and it's never that crowded. Busch dining gets a bad reputation but it's fine, nothing special though. Neilson dining hall has really improved since they switched to whole foods and removed processed stuff like cold cuts and chicken nuggets. Overall Rutgers dining is better than most schools I visited during my college search.""",
    "src_06": """Livingston dining hall tour at Rutgers University. The dining hall is huge and has so many options. First station is the Mongolian grill where you pick your own ingredients and they cook it in front of you. There is also a coconut milk ramen station which is so good. The salad bar is massive with tons of toppings. They have a deli station, a hot entree station, pizza, burgers, and a dessert section with soft serve ice cream. The soft serve is honestly the highlight, students are obsessed with it. Livingston dining is open late which is great for students who have night classes on Livingston campus. Overall Livingston is considered the best dining hall at Rutgers by most students.""",
    "src_07": """Stuff Yer Face is a Rutgers institution, been around since 1977. Famous for their strombolis which are massive and delicious. Located on Easton Ave right near College Ave campus. Very popular with students especially late night. Prices are reasonable for the portion size. Harvest Moon Brewery and Cafe is a great spot in downtown New Brunswick. Good burgers and craft beers. A little pricier than typical student budget but worth it for a special occasion. About a 10 minute walk from College Ave campus. Ramen Nagomi is the best ramen in New Brunswick. Authentic Japanese ramen with rich broth. Students love this place. Can get crowded on weekends so go early. Located on George Street downtown. Indochine is a Vietnamese restaurant on Albany Street. Great pho and banh mi sandwiches at very affordable prices. Very popular with Rutgers students. Cash only so bring cash. Old Man Rafferty's is a classic American comfort food restaurant in downtown New Brunswick. Known for huge portions and a varied menu. Good for groups.""",
    "src_10": """What is the best dining hall at Rutgers? Livingston is the best no competition. The Mongolian station and the ramen are insane. Also the soft serve. Cook Doug is slept on honestly, the food is really good and it is never packed. Neilson is okay but it has gotten better since they changed the menu. Busch dining is mid but it is convenient if you live on Busch. The Atrium on College Ave is the worst, overpriced and only 3 swipes a day. Can I use meal swipes at the Atrium? Yes you can use meal swipes at the Atrium but there is a 3 swipe per day limit. After that you need to use RU Express or pay cash. Does the Starbucks truck take meal swipes? Yes the Starbucks truck accepts meal swipes and it has the full Starbucks menu including food items like sandwiches and pastries. It rotates between campuses on a weekly schedule. Monday is College Ave by Alexander Library, Tuesday is Livingston by the towers, Wednesday is Cook by Biel Road, Thursday is Busch by Allison Road Classrooms, Friday is George Street by the River Dorms. Henry's Diner on Livingston is so underrated. They have pancakes the size of your face and they accept meal swipes. What dining halls are good for vegetarians? Neilson has really good vegetarian options since they overhauled the menu. Livingston also has a solid salad bar. Most dining halls have at least one vegetarian entree at every meal.""",
}

# ---------------------------------------------------------------------------
# STAGE 2 — CHUNKING
# ---------------------------------------------------------------------------

# Use cl100k_base tokenizer (same family as GPT-4 / Claude) — good proxy
# for token counts regardless of which LLM you use downstream.
_tokenizer = tiktoken.get_encoding("cl100k_base")


def _count_tokens(text: str) -> int:
    return len(_tokenizer.encode(text))


def _split_into_paragraphs(text: str) -> list[str]:
    """Split on double newlines, returning non-empty paragraphs."""
    return [p.strip() for p in re.split(r"\n\n+", text) if p.strip()]


def chunk_text(
    text: str,
    source_id: str,
    source_name: str,
    source_type: str,
    chunk_size: int = 250,      # target tokens per chunk (spec: 200-300)
    overlap: int = 30,           # overlap tokens (spec: 30)
    min_chunk_tokens: int = 20,  # discard tiny fragments
) -> list[dict]:
    """
    Split cleaned text into overlapping token-bounded chunks.

    Strategy (matches your planning.md):
    1. Split on paragraph boundaries first (respect content structure).
    2. If a paragraph fits within chunk_size, accumulate it.
    3. If adding the next paragraph would exceed chunk_size, flush the current
       chunk and start a new one seeded with the overlap tail of the previous.
    4. If a single paragraph exceeds chunk_size, split it at sentence boundaries.

    Each chunk dict has keys:
        text        — the chunk content
        source_id   — e.g. "src_01"
        source_name — human-readable source label
        source_type — "official" | "student_review" | "news" | "curated" | "review"
        chunk_id    — globally unique id, e.g. "src_01_c00"
        token_count — number of tokens in the chunk
    """
    paragraphs = _split_into_paragraphs(text)
    if not paragraphs:
        return []

    chunks: list[dict] = []
    chunk_index = 0

    current_tokens: list[int] = []   # token ids of current chunk
    current_text_parts: list[str] = []

    def flush_chunk():
        nonlocal chunk_index
        chunk_text_str = " ".join(current_text_parts).strip()
        token_count = len(current_tokens)
        if token_count < min_chunk_tokens:
            return  # discard near-empty fragments
        chunks.append({
            "text": chunk_text_str,
            "source_id": source_id,
            "source_name": source_name,
            "source_type": source_type,
            "chunk_id": f"{source_id}_c{chunk_index:02d}",
            "token_count": token_count,
        })
        chunk_index += 1

    def get_overlap_seed(token_ids: list[int]) -> tuple[list[int], str]:
        """Return the last `overlap` tokens as (token_ids, decoded_text)."""
        tail_ids = token_ids[-overlap:] if len(token_ids) > overlap else token_ids
        tail_text = _tokenizer.decode(tail_ids)
        return tail_ids, tail_text

    def split_paragraph_by_sentences(para: str) -> list[str]:
        """Fallback: split an oversized paragraph at sentence boundaries."""
        sentences = re.split(r'(?<=[.!?])\s+', para)
        groups: list[str] = []
        current: list[str] = []
        current_tok = 0
        for sent in sentences:
            sent_tok = _count_tokens(sent)
            if current_tok + sent_tok > chunk_size and current:
                groups.append(" ".join(current))
                current = [sent]
                current_tok = sent_tok
            else:
                current.append(sent)
                current_tok += sent_tok
        if current:
            groups.append(" ".join(current))
        return groups

    for para in paragraphs:
        para_token_ids = _tokenizer.encode(para)
        para_token_count = len(para_token_ids)

        # Oversized single paragraph — split by sentences first
        if para_token_count > chunk_size:
            sub_paras = split_paragraph_by_sentences(para)
        else:
            sub_paras = [para]

        for sub in sub_paras:
            sub_ids = _tokenizer.encode(sub)
            sub_count = len(sub_ids)

            if len(current_tokens) + sub_count > chunk_size and current_tokens:
                # Flush current chunk
                flush_chunk()
                # Seed new chunk with overlap from the end of the flushed chunk
                overlap_ids, overlap_text = get_overlap_seed(current_tokens)
                current_tokens = list(overlap_ids)
                current_text_parts = [overlap_text] if overlap_text.strip() else []

            current_tokens.extend(sub_ids)
            current_text_parts.append(sub)

    # Flush any remaining content
    if current_tokens:
        flush_chunk()

    return chunks


# ---------------------------------------------------------------------------
# STAGE 3 — BUILD CORPUS
# ---------------------------------------------------------------------------

def build_corpus(sources: list[dict] = SOURCES, delay_between_requests: float = 1.5) -> list[dict]:
    """
    Run ingestion + chunking across all sources.
    Returns flat list of all chunk dicts.
    """
    all_chunks: list[dict] = []

    for source in sources:
        sid = source["id"]
        sname = source["name"]
        stype = source["type"]
        url = source["url"]

        print(f"\n[{sid}] Fetching: {sname}")
        print(f"  URL: {url}")

        text = fetch_and_clean(url, source_id=sid)

        if not text:
            print(f"  [SKIP] No usable text retrieved for {sid}.")
            print(f"  ACTION: Manually copy text for this source and add it to FALLBACK_TEXTS[\"{sid}\"]")
            continue

        print(f"  Cleaned text length: {len(text)} chars / ~{_count_tokens(text)} tokens")

        chunks = chunk_text(
            text=text,
            source_id=sid,
            source_name=sname,
            source_type=stype,
        )

        print(f"  Produced {len(chunks)} chunks")
        all_chunks.extend(chunks)

        # Be polite to servers
        time.sleep(delay_between_requests)

    return all_chunks


# ---------------------------------------------------------------------------
# STAGE 4 — INSPECTION
# ---------------------------------------------------------------------------

def inspect_chunks(chunks: list[dict], n: int = 5) -> None:
    """
    Print n random chunks for manual review.
    Use this to verify chunks are substantive and self-contained.
    """
    print("\n" + "=" * 70)
    print(f"CHUNK INSPECTION — {n} random samples from {len(chunks)} total")
    print("=" * 70)

    sample = random.sample(chunks, min(n, len(chunks)))

    for i, chunk in enumerate(sample, 1):
        print(f"\n--- Chunk {i} | {chunk['chunk_id']} | {chunk['token_count']} tokens ---")
        print(f"Source: {chunk['source_name']} [{chunk['source_type']}]")
        print(f"Text:\n{chunk['text']}")
        print()

    # Summary stats
    token_counts = [c["token_count"] for c in chunks]
    print("=" * 70)
    print(f"SUMMARY")
    print(f"  Total chunks:      {len(chunks)}")
    print(f"  Min tokens/chunk:  {min(token_counts)}")
    print(f"  Max tokens/chunk:  {max(token_counts)}")
    print(f"  Avg tokens/chunk:  {sum(token_counts) / len(token_counts):.1f}")

    # Source breakdown
    from collections import Counter
    source_counts = Counter(c["source_id"] for c in chunks)
    print(f"\n  Chunks per source:")
    for sid, count in sorted(source_counts.items()):
        sname = next(s["name"] for s in SOURCES if s["id"] == sid)
        print(f"    {sid}: {count:3d}  {sname[:55]}")
    print("=" * 70)


# ---------------------------------------------------------------------------
# SAVE / LOAD HELPERS
# ---------------------------------------------------------------------------

def save_chunks(chunks: list[dict], path: str = "chunks.json") -> None:
    """Save chunk list to JSON for reuse in Milestone 4."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"\nSaved {len(chunks)} chunks to {path}")


def load_chunks(path: str = "chunks.json") -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Milestone 3: Rutgers Dining RAG — Document Pipeline ===\n")

    # Build corpus
    chunks = build_corpus(SOURCES)

    if not chunks:
        print("\n[ERROR] No chunks produced. Check FALLBACK_TEXTS for blocked sources.")
    else:
        # Inspect
        inspect_chunks(chunks, n=5)

        # Persist for Milestone 4
        save_chunks(chunks, "chunks.json")

        print("\n✅  Milestone 3 complete.")
        print("   Next: use chunks.json as input to Milestone 4 (embedding + ChromaDB).")