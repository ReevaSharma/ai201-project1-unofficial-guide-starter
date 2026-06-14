"""
Milestone 4 — Embedding, Vector Store, and Retrieval
Rutgers Dining Unofficial Guide RAG Pipeline

Stages:
  1. build_index(chunks)        — embed all chunks, store in ChromaDB
  2. retrieve(query, k)         — query vector store, return top-k chunks
  3. test_retrieval()           — run 3 evaluation questions, print results
"""

import json
from typing import Optional

# ---------------------------------------------------------------------------
# Dependencies (install with):
#   pip install sentence-transformers chromadb
# ---------------------------------------------------------------------------

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    raise ImportError("Run: pip install sentence-transformers")

try:
    import chromadb
except ImportError:
    raise ImportError("Run: pip install chromadb")


# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

CHUNKS_FILE = "chunks.json"
CHROMA_DIR = "./chroma_db"        # ChromaDB persists to disk here
COLLECTION_NAME = "rutgers_dining"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_K = 5


# ---------------------------------------------------------------------------
# LOAD CHUNKS
# ---------------------------------------------------------------------------

def load_chunks(path: str = CHUNKS_FILE) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# STAGE 1 — BUILD INDEX
# ---------------------------------------------------------------------------

def build_index(chunks: list[dict], reset: bool = False) -> chromadb.Collection:
    """
    Embed all chunks with all-MiniLM-L6-v2 and store in ChromaDB.

    Args:
        chunks:  list of chunk dicts from pipeline.py
        reset:   if True, wipe and rebuild the collection from scratch

    Returns:
        ChromaDB collection ready for querying
    """
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Persistent ChromaDB client — data survives between runs
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Reset collection if requested or if it doesn't exist
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"Deleted existing collection: {COLLECTION_NAME}")
        except Exception:
            pass

    # Get or create collection
    # ChromaDB stores embeddings + metadata + documents together
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},  # cosine distance (lower = more similar)
    )

    # Skip re-embedding if collection already has data
    existing_count = collection.count()
    if existing_count > 0 and not reset:
        print(f"Collection already has {existing_count} chunks — skipping embedding.")
        print("Pass reset=True to rebuild from scratch.")
        return collection

    print(f"\nEmbedding {len(chunks)} chunks...")

    # Embed in batches for efficiency
    batch_size = 32
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]

        texts = [c["text"] for c in batch]
        ids = [c["chunk_id"] for c in batch]

        # Metadata stored alongside each embedding — used for attribution later
        metadatas = [
            {
                "source_id": c["source_id"],
                "source_name": c["source_name"],
                "source_type": c["source_type"],
                "token_count": c["token_count"],
            }
            for c in batch
        ]

        # Generate embeddings (returns numpy array)
        embeddings = model.encode(texts, show_progress_bar=False).tolist()

        # Add to ChromaDB
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,        # store raw text for retrieval
            metadatas=metadatas,
        )

        print(f"  Embedded chunks {i+1}–{min(i+batch_size, len(chunks))} of {len(chunks)}")

    print(f"\nIndex built. Total chunks in store: {collection.count()}")
    return collection


# ---------------------------------------------------------------------------
# STAGE 2 — RETRIEVAL
# ---------------------------------------------------------------------------

# Load model once at module level so retrieve() doesn't reload it each call
_model: Optional[SentenceTransformer] = None

def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def get_collection() -> chromadb.Collection:
    """Get the existing ChromaDB collection."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(COLLECTION_NAME)


def retrieve(query: str, k: int = DEFAULT_K) -> list[dict]:
    """
    Embed the query and return the top-k most similar chunks.

    Each returned dict has:
        text        — chunk content
        source_name — human-readable source label
        source_type — official | student_review | news | etc.
        source_id   — e.g. src_01
        chunk_id    — e.g. src_01_c03
        distance    — cosine distance (0 = identical, 1 = unrelated)
    """
    model = _get_model()
    collection = get_collection()

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    # Unpack ChromaDB result structure
    chunks_out = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks_out.append({
            "text": doc,
            "source_name": meta["source_name"],
            "source_type": meta["source_type"],
            "source_id": meta["source_id"],
            "chunk_id": meta.get("chunk_id", ""),
            "distance": round(dist, 4),
        })

    return chunks_out


# ---------------------------------------------------------------------------
# STAGE 3 — RETRIEVAL TESTING
# ---------------------------------------------------------------------------

# 3 of your 5 evaluation questions for testing
TEST_QUERIES = [
    {
        "id": "Q1",
        "question": "What are students' opinions about Livingston dining compared to the Atrium on College Avenue?",
        "expect": "Livingston praised (soft serve, Asian station), Atrium criticized (3-swipe cap)",
    },
    {
        "id": "Q4",
        "question": "Does Rutgers have a Starbucks truck, and how does it work?",
        "expect": "Yes, accepts meal swipes, rotates campuses weekly",
    },
    {
        "id": "Q5",
        "question": "What can students with dietary restrictions eat at Neilson Dining Hall?",
        "expect": "Gluten-free, vegetarian, whole foods, roasted meats, no processed food",
    },
]


def test_retrieval(k: int = DEFAULT_K) -> None:
    """
    Run test queries and print retrieved chunks with distance scores.
    Use this to verify retrieval quality before Milestone 5.
    """
    print("\n" + "=" * 70)
    print("RETRIEVAL TEST — 3 evaluation queries")
    print("=" * 70)

    for test in TEST_QUERIES:
        print(f"\n{'─' * 70}")
        print(f"{test['id']}: {test['question']}")
        print(f"Expected: {test['expect']}")
        print(f"{'─' * 70}")

        chunks = retrieve(test["question"], k=k)

        for i, chunk in enumerate(chunks, 1):
            # Flag potentially weak matches
            quality = "✅" if chunk["distance"] < 0.5 else "⚠️  HIGH DISTANCE"
            print(f"\n  Result {i} | distance: {chunk['distance']} {quality}")
            print(f"  Source: {chunk['source_name']} [{chunk['source_type']}]")
            print(f"  Text: {chunk['text'][:300]}{'...' if len(chunk['text']) > 300 else ''}")

        # Summary for this query
        distances = [c["distance"] for c in chunks]
        print(f"\n  Distance range: {min(distances):.4f} – {max(distances):.4f}")
        if min(distances) > 0.5:
            print("  ⚠️  WARNING: Best match has distance > 0.5 — retrieval may be weak.")
            print("     Check: are chunks too short? Is the query term in any chunk?")

    print("\n" + "=" * 70)
    print("RETRIEVAL TEST COMPLETE")
    print("If results look relevant, you're ready for Milestone 5.")
    print("If results look off, debug chunk content or adjust chunk size.")
    print("=" * 70)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Milestone 4: Rutgers Dining RAG — Embedding & Retrieval ===\n")

    # Load chunks from Milestone 3
    chunks = load_chunks(CHUNKS_FILE)
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_FILE}")

    # Build the vector index
    # Set reset=True if you want to rebuild from scratch
    collection = build_index(chunks, reset=False)

    # Test retrieval with evaluation queries
    test_retrieval()

    print("\n✅  Milestone 4 complete.")
    print("   Next: use retrieve() in Milestone 5 for grounded generation.")