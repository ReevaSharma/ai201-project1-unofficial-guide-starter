"""
Milestone 5 — Grounded Generation + Gradio Interface
Rutgers Dining Unofficial Guide RAG Pipeline

Usage:
    python app.py
    Then open http://localhost:7860
"""

import os
from retrieve import retrieve  # reuse Milestone 4 retrieval

# ---------------------------------------------------------------------------
# Dependencies (install with):
#   pip install groq gradio python-dotenv
# ---------------------------------------------------------------------------

try:
    from groq import Groq
except ImportError:
    raise ImportError("Run: pip install groq")

try:
    import gradio as gr
except ImportError:
    raise ImportError("Run: pip install gradio")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # if no .env file, GROQ_API_KEY must be set in environment


# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 1000
TOP_K = 5

client = Groq()  # reads GROQ_API_KEY from environment


# ---------------------------------------------------------------------------
# SYSTEM PROMPT — enforces grounding
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are the Rutgers University–New Brunswick Unofficial Dining Guide assistant.

Your job is to answer student questions about campus dining using ONLY the source documents provided in each message.

STRICT RULES:
1. Answer ONLY from the provided documents. Do not use your general training knowledge about Rutgers, dining halls, or New Brunswick restaurants.
2. If the documents do not contain enough information to answer the question, say exactly: "I don't have enough information on that in my sources."
3. Always end your response with a "Sources:" section that lists every document you drew from, using the exact source names provided.
4. When documents conflict (e.g. official site vs student review), note the conflict explicitly — for example: "The official site says X, but students report Y."
5. Keep your tone friendly and practical, like a helpful upperclassman giving advice.

FORMAT:
[Your answer in 2-4 sentences]

Sources:
• [Source name]
• [Source name]
"""


# ---------------------------------------------------------------------------
# GROUNDED GENERATION
# ---------------------------------------------------------------------------

def format_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a context block for the prompt."""
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[Document {i}]\n"
            f"Source: {chunk['source_name']} (type: {chunk['source_type']})\n"
            f"Content: {chunk['text']}"
        )
    return "\n\n".join(parts)


def ask(question: str, k: int = TOP_K) -> dict:
    """
    Full RAG pipeline: retrieve → format context → generate grounded answer.

    Returns:
        {
            "answer":   str,         — grounded response text
            "sources":  list[str],   — unique source names used
            "chunks":   list[dict],  — raw retrieved chunks (for debugging)
        }
    """
    # Step 1: Retrieve relevant chunks
    chunks = retrieve(question, k=k)

    # Step 2: Format context
    context = format_context(chunks)

    # Step 3: Build user message with context + question
    user_message = f"""Here are the relevant documents from the Rutgers dining guide:

{context}

---

Student question: {question}

Remember: answer ONLY from the documents above. If they don't cover this question, say so."""

    # Step 4: Call Groq API
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    answer = response.choices[0].message.content

    # Step 5: Collect unique source names from retrieved chunks
    # (programmatic attribution — guaranteed regardless of LLM output)
    seen = set()
    sources = []
    for chunk in chunks:
        if chunk["source_name"] not in seen:
            seen.add(chunk["source_name"])
            sources.append(chunk["source_name"])

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
    }


# ---------------------------------------------------------------------------
# GRADIO INTERFACE
# ---------------------------------------------------------------------------

def handle_query(question: str):
    """Gradio handler — calls ask() and formats output for the UI."""
    if not question.strip():
        return "Please enter a question.", ""

    try:
        result = ask(question)
        answer = result["answer"]
        sources = "\n".join(f"• {s}" for s in result["sources"])
        return answer, sources
    except Exception as e:
        return f"Error: {str(e)}", ""


EXAMPLES = [
    "What are students' opinions about Livingston dining compared to the Atrium?",
    "Does Rutgers have a Starbucks truck, and how does it work?",
    "Can I use my meal swipe at the Busch student center?",
    "What are some budget-friendly places to eat near College Avenue?",
    "What can students with dietary restrictions eat at Neilson Dining Hall?",
]

with gr.Blocks(title="Rutgers Dining Unofficial Guide") as demo:
    gr.Markdown(
        """
        # 🍽️ Rutgers Dining — Unofficial Guide
        Ask anything about campus dining halls, meal swipes, food trucks, or nearby restaurants.
        Answers are grounded in student reviews and official Rutgers sources.
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            question_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. Which dining hall has the best food?",
                lines=2,
            )
            ask_btn = gr.Button("Ask", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("**Try these:**")
            for ex in EXAMPLES:
                gr.Button(ex, size="sm").click(
                    fn=lambda q=ex: q,
                    outputs=question_box,
                )

    answer_box = gr.Textbox(label="Answer", lines=8, interactive=False)
    sources_box = gr.Textbox(label="Retrieved from", lines=4, interactive=False)

    ask_btn.click(
        fn=handle_query,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )
    question_box.submit(
        fn=handle_query,
        inputs=question_box,
        outputs=[answer_box, sources_box],
    )


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Milestone 5: Testing grounded generation ===\n")

    test_questions = [
        "What are students' opinions about Livingston dining compared to the Atrium?",
        "Does Rutgers have a Starbucks truck, and how does it work?",
        "What is the best pizza place in Tokyo?",  # out-of-scope — should decline
    ]

    for q in test_questions:
        print(f"Q: {q}")
        result = ask(q)
        print(f"A: {result['answer']}")
        print(f"Sources: {', '.join(result['sources'])}")
        print()

    print("Launching Gradio interface at http://localhost:7860 ...\n")
    demo.launch() 