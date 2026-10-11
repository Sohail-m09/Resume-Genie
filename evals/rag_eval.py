"""
Resume Genie: Simple RAG Evaluation
Measures:
  1. Retrieval Accuracy: Hit@1, Hit@3, MRR
  2. Generation Fidelity: hallucination rate using an LLM fact-checker

Run from the PROJECT ROOT (PowerShell):
    $env:PYTHONPATH="app"
    python evals/rag_eval.py
"""
import os
import json
import time
from retrieval.chroma_retriever import retrieve_resume_context
from rag.context_builder import build_resume_context
from analysis.career_coach_prompt import build_career_coach_prompt
from llm.gemini import get_gemini_model

# 1. SETTINGS & TEST DATASET
USER_ID = 43       # change to a stored resume id
RESUME_ID = 42
TOP_K = 3

EVAL_SET = [
    {"question": "What is the candidate's CGPA?", "expected_keywords": ["7.01"], "answerable": True},
    {"question": "Which project reached 94% accuracy?", "expected_keywords": ["94%"], "answerable": True},
    {"question": "Which tools did the Bank Loan Prediction project use?", "expected_keywords": ["Snowflake"], "answerable": True},
    {"question": "Which certifications does the candidate have?", "expected_keywords": ["Deloitte"], "answerable": True},
    {"question": "Which databases does the candidate know?", "expected_keywords": ["PostgreSQL"], "answerable": True},
    {"question": "Which data visualization tools are listed?", "expected_keywords": ["Tableau"], "answerable": True},
    {"question": "What was used for data versioning in the cement project?", "expected_keywords": ["DVC"], "answerable": True},
    {"question": "What is the higher secondary percentage?", "expected_keywords": ["85.5"], "answerable": True},
    {"question": "Summarise the professional summary.", "expected_keywords": ["business problems"], "answerable": True},
    {"question": "What does the phishing project do?", "expected_keywords": ["phishing"], "answerable": True},
    # Trap questions: the resume does not contain these, so the system must say "unavailable"
    {"question": "Does the candidate have Kubernetes experience?", "expected_keywords": [], "answerable": False},
    {"question": "What is the candidate's current salary?", "expected_keywords": [], "answerable": False},
    {"question": "Did the candidate work at Google?", "expected_keywords": [], "answerable": False},
]

# Simple LLM judge prompt to detect hallucinations
FACT_CHECK_PROMPT = """
Context:
{context}

Answer:
{answer}

Question: Does the answer contain any claim not backed by the context?
Respond in strictly valid JSON: {{"faithful": true or false, "reason": "brief reason"}}
"""


def to_text(response):
    """Gemini can return a list of blocks (with 'type', 'extras', 'signature').
    Keep only the text, otherwise that metadata pollutes the answer being judged."""
    content = response.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict))
    return str(content)


def call_model(model, prompt):
    """Call Gemini; if it fails (rate limit), wait and try again up to 3 times."""
    for attempt in range(3):
        try:
            return to_text(model.invoke(prompt))
        except Exception as error:
            print(f"  model call failed ({error}); retrying in 15 seconds...")
            time.sleep(15)
    return ""


def find_keyword_rank(retrieved_chunks, keywords):
    """Finds which chunk rank (1, 2 or 3) contains all the expected keywords."""
    if not keywords:
        return None
    for rank, chunk in enumerate(retrieved_chunks, start=1):
        chunk_text = chunk["text"].lower().replace(" ", "")   # ignore PDF spacing quirks
        if all(kw.lower().replace(" ", "") in chunk_text for kw in keywords):
            return rank
    return None  # None means the keywords were not found in the top-k chunks


def fact_check(model, context, answer):
    """Asks the model if the answer contains any claim outside the context."""
    text = call_model(model, FACT_CHECK_PROMPT.format(context=context, answer=answer))
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except Exception:
        return {"faithful": False, "reason": "Could not parse JSON output"}


def main():
    model = get_gemini_model()
    os.makedirs("evals", exist_ok=True)
    results = []

    print(f"Starting evaluation on {len(EVAL_SET)} questions...\n")

    for item in EVAL_SET:
        query = item["question"]

        # Step 1: Retrieval (same function the app uses)
        chunks = retrieve_resume_context(query, top_k=TOP_K, user_id=USER_ID, resume_id=RESUME_ID)
        rank = find_keyword_rank(chunks, item["expected_keywords"]) if item["answerable"] else None

        # Step 2: Generation (same prompt builder and model as the app)
        context = build_resume_context(chunks)
        coach_prompt = build_career_coach_prompt(question=query, resume_context=context)
        answer = call_model(model, coach_prompt)

        # Step 3: Fact-checking
        verdict = fact_check(model, context, answer)

        results.append({
            "question": query,
            "answerable": item["answerable"],
            "rank": rank,
            "contexts": [c["text"] for c in chunks],
            "answer": answer,
            "faithful": verdict.get("faithful", False),
            "reason": verdict.get("reason", ""),
        })

        print(f"Processed: {query}")
        time.sleep(2)  # avoid rate limits

    # --- Print summary metrics ---
    answerable = [r for r in results if r["answerable"]]
    traps = [r for r in results if not r["answerable"]]
    total_ans = max(len(answerable), 1)

    hit_1 = sum(1 for r in answerable if r["rank"] == 1) / total_ans
    hit_k = sum(1 for r in answerable if r["rank"] is not None) / total_ans
    mrr = sum(1.0 / r["rank"] for r in answerable if r["rank"]) / total_ans
    faithfulness = sum(1 for r in answerable if r["faithful"]) / total_ans
    trap_success = sum(1 for r in traps if r["faithful"]) / max(len(traps), 1)

    print("\n" + "=" * 40)
    print("           EVALUATION SUMMARY")
    print("=" * 40)
    print(f"Hit@1 (First chunk accuracy):   {hit_1:.2%}")
    print(f"Hit@{TOP_K} (Top-{TOP_K} recall):           {hit_k:.2%}")
    print(f"MRR (Mean Reciprocal Rank):     {mrr:.2f}")
    print(f"Answer Faithfulness:            {faithfulness:.2%}")
    print(f"Trap / Hallucination Handling:  {trap_success:.2%}")
    print("=" * 40)

    for r in results:
        if not r["faithful"]:
            print("CHECK THIS ONE:", r["question"], "->", r["reason"])

    # Save for the RAGAS evaluation
    with open("evals/results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Results saved to evals/results.json")


if __name__ == "__main__":
    main()
