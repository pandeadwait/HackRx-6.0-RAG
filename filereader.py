import os
from PyPDF2 import PdfReader
from docx import Document
from langchain.text_splitter import CharacterTextSplitter

def getPdfChunks(filename):
    text = ""
    pages = PdfReader(filename)

    for page in pages.pages:
        text += page.extract_text()
    
    splitter = CharacterTextSplitter(separator = '\n', chunk_size = 1000, chunk_overlap = 200, length_function = len)

    chunks = splitter.spilt_text(text)

    return chunks

def getDocxChunks(filename):
    doc = Document(filename)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]

    text = ""
    for paragraph in paragraphs:
        text += paragraph

    splitter = CharacterTextSplitter(separator = '\n', chunk_size = 1000, chunk_overlap = 200, length_function = len)

    chunks = splitter.split_text(text)

    return chunks

def chunker(filename):
    extension = os.path.splitext(filename)[-1].lower()
    chunks = list()

    if extension == ".pdf":
        chunk = getPdfChunks(filename)
    elif extension == '.docx':
        chunk = getDocxChunks(filename)
    
    return chunks