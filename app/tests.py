from rag.context_builder import build_resume_context

retrieved_chunks = [
    {
        "text": "Built a phishing detection model using Python and scikit-learn.",
        "metadata": {
            "source": "resume.pdf",
            "page": 2,
            "page_label": "2"
        },
        "distance": 0.21
    },
    {
        "text": "Developed a depression prediction model using machine learning.",
        "metadata": {
            "source": "resume.pdf",
            "page": 3,
            "page_label": "3"
        },
        "distance": 0.29
    }
]


context = build_resume_context(retrieved_chunks)

print("===== GENERATED CONTEXT =====")
print(context)