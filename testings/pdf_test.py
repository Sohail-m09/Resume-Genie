'''
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/example.pdf")

documents = loader.load()

print("Number of pages:", len(documents))

for document in documents:
    print("\n--- PAGE ---")
    print(document.page_content)
    print("Metadata:", document.metadata)
'''
'''
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/example.pdf")

documents = loader.load()

print("Number of documents:", len(documents))

for i, document in enumerate(documents):
    print(f"\n===== DOCUMENT {i + 1} =====")

    print("\nType:")
    print(type(document))

    print("\nPage Content:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)
type(document)
document.page_content
document.metadata'''


from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/example.pdf")
documents = loader.load()

raw_text = "\n".join(
    document.page_content
    for document in documents
)

print("===== RAW TEXT =====")
print(repr(raw_text[:1000]))