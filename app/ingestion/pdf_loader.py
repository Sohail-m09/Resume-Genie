from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def load_pdf(file_path : str) -> list[Document]:
    loader = PyPDFLoader(file_path)
    return loader.load()

''' 
Loads a pdf file and return it's pages ad langchain documents 
Returns a list of Document objects, usually one per page
'''