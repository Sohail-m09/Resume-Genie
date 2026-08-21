from langchain_core.documents import Document

def extract_text(documents: list[Document]) -> str:
    return "\n".join(
        document.page_content
        for document in documents
    ) 
'''
Combine the text content from multiple Document objects.
documents: LangChain Document objects produced by the PDF loader.
Returns:
Combined raw text.
'''