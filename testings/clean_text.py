from langchain_community.document_loaders import PyPDFLoader

from text_utils import clean_text


loader = PyPDFLoader("data/Sohail_Momin.pdf")
documents = loader.load()

raw_text = "\n".join(
    document.page_content
    for document in documents
)

cleaned_text = clean_text(raw_text)

print("===== CLEANED TEXT =====")
print(cleaned_text)