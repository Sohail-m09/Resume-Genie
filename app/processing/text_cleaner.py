import re
from langchain_core.documents import Document

def clean_text(text : str) -> str:
    text = text.replace("\t" , " ")
    text = re.sub(r"[ ]+" , " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

## Now we are making another function for preserving the metadata also

def clean_documents(documents: list[Document]) -> list[Document]:
    cleaned_documents = []
    for document in documents:
        cleaned_document = Document(
            page_content=clean_text(document.page_content),
            metadata=document.metadata.copy(),
        )
        cleaned_documents.append(cleaned_document)
    return cleaned_documents
'''
Conservatively normalize whitespaces in extracted document text
text : Raw extracted text
Returns cleaned text
'''