import os
import io
import zipfile
import email
from email import policy
from PyPDF2 import PdfReader
from docx import Document
from langchain.text_splitter import CharacterTextSplitter

def getPdfChunks(filename):
    text = ""
    pages = PdfReader(filename)

    for page in pages.pages:
        text += page.extract_text()
    
    splitter = CharacterTextSplitter(separator = '\n', chunk_size = 1000, chunk_overlap = 200, length_function = len)

    chunks = splitter.split_text(text)

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

def getEmailChunks(filename):
    with open(filename, 'rb') as fp:
        msg = email.message_from_binary_file(fp, policy=policy.default)

    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    text += payload.decode('utf-8')
    else:
        if msg.get_content_type() == 'text/plain':
            payload = msg.get_payload(decode=True)
            if payload:
                text += payload.decode('utf-8')

    text = text.strip()

    if not text:
        return []

    splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = splitter.split_text(text)

    return chunks

def getDocType(document: bytes) -> str:
    # Check for PDF by its magic number
    if document.startswith(b"%PDF"):
        return "pdf"
    
    # Check for email by common headers
    text = document.decode('utf-8', errors='ignore')
    if "From:" in text and "Subject:" in text:
        return "email"

    # Check for DOCX by treating it as a ZIP file
    try:
        with zipfile.ZipFile(io.BytesIO(document)) as z:
            if "word/document.xml" in z.namelist():
                return "docx"
    except zipfile.BadZipFile:
        pass  # Not a zip file, so not a DOCX

    return "Unknown"

def chunker(filename):
    # extension = os.path.splitext(filename)[-1].lower()
    chunks = list()

    type = getDocType(filename)

    if type == "pdf":
        chunks= getPdfChunks(filename)
    elif type == "docx":
        chunks = getDocxChunks(filename)
    elif type == "email":
        chunks = getEmailChunks(filename)

    # if extension == ".pdf":
    #     chunks= getPdfChunks(filename)
    # elif extension == '.docx':
    #     chunks = getDocxChunks(filename)
    
    return chunks