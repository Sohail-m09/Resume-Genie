from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_documents(
        documents : list[Document],
        chunk_size : int = 1000,
        chunk_overlap : int = 200,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
    )
    return splitter.split_documents(documents)

'''
Split text into overlapping chunks
        text: Cleaned document text.
        chunk_size: Target maximum chunk size.
        chunk_overlap: Amount of overlap between neighbouring chunks.
        Retruns a list of text chunks.
'''