"""
Resume Genie: RAGAS-style evaluation WITHOUT the ragas library.

Use this if `pip install ragas` conflicts with your LangChain packages.
It scores the same three ideas RAGAS scores, using your own Gemini model as the judge:

  faithfulness       = share of the answer's claims that the retrieved chunks support
  answer_relevancy   = does the answer address the question?   (1 / 0.5 / 0)
  context_precision  = share of retrieved chunks that are relevant to the question

It reads evals/results.json (made by rag_eval.py), so it makes no new retrieval
or answer-generation calls. Only judge calls.

Run from the PROJECT ROOT (PowerShell):
    $env:PYTHONPATH="app"
    python evals\\ragas_style_eval.py
"""
import csv
import json
import os
import time
from llm.gemini import get_gemini_model

FAITHFULNESS_PROMPT = """
Context:
{context}

Answer:
{answer}

Split the Answer into separate factual claims. Count how many claims are supported by the Context.
Respond in strictly valid JSON: {{"total_claims": <number>, "supported_claims": <number>}}
"""

RELEVANCY_PROMPT = """
Question:
{question}

Answer:
{answer}

Does the Answer directly address the Question?
Score 1 if fully, 0.5 if partly, 0 if not at all.
Respond in strictly valid JSON: {{"score": <1 or 0.5 or 0>}}
"""

CONTEXT_PROMPT = """
Question:
{question}

Chunks:
{chunks}

For each numbered chunk, say whether it helps answer the Question.
Respond in strictly valid JSON: {{"relevant": [true, false, ...]}}  (one value per chunk, in order)
"""


def to_text(response):
    """Keep only the text if Gemini returns a list of blocks."""
    content = response.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict))
    return str(content)


def ask_json(model, prompt):
    """Ask Gemini for JSON. Retry 3 times if the call fails. Return {} if unreadable."""
    for _ in range(3):
        try:
            text = to_text(model.invoke(prompt))
            return json.loads(text[text.find("{"): text.rfind("}") + 1])
        except Exception as error:
            print(f"  judge call failed ({error}); retrying in 15 seconds...")
            time.sleep(15)
    return {}


def main():
    path = "evals/results.json"
    if not os.path.exists(path):
        print("Please run evals/rag_eval.py first to generate results.json!")
        return

    rows = [r for r in json.load(open(path, encoding="utf-8")) if r["answerable"]]
    model = get_gemini_model()
    scores = []

    for r in rows:
        context = "\n\n".join(r["contexts"])
        chunks = "\n\n".join(f"[{i}] {c}" for i, c in enumerate(r["contexts"], start=1))

        f = ask_json(model, FAITHFULNESS_PROMPT.format(context=context, answer=r["answer"]))
        total = f.get("total_claims") or 0
        faithfulness = (f.get("supported_claims", 0) / total) if total else None

        relevancy = ask_json(model, RELEVANCY_PROMPT.format(question=r["question"], answer=r["answer"])).get("score")

        flags = ask_json(model, CONTEXT_PROMPT.format(question=r["question"], chunks=chunks)).get("relevant")
        precision = (sum(1 for x in flags if x) / len(flags)) if flags else None

        scores.append({
            "question": r["question"],
            "faithfulness": faithfulness,
            "answer_relevancy": relevancy,
            "context_precision": precision,
        })
        print("scored:", r["question"])
        time.sleep(2)  # avoid rate limits

    def average(key):
        values = [s[key] for s in scores if s[key] is not None]
        return sum(values) / len(values) if values else float("nan")

    print("\n" + "=" * 40)
    print(" RAGAS-STYLE SCORES (0.0 - 1.0)")
    print("=" * 40)
    print(f"faithfulness      : {average('faithfulness'):.2f}")
    print(f"answer_relevancy  : {average('answer_relevancy'):.2f}")
    print(f"context_precision : {average('context_precision'):.2f}")
    print("=" * 40)

    with open("evals/ragas_style_scores.csv", "w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=list(scores[0].keys()))
        writer.writeheader()
        writer.writerows(scores)
    print("Detailed scores saved to evals/ragas_style_scores.csv (check the lowest rows)")


if __name__ == "__main__":
    main()