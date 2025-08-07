import io
import zipfile
import email
from email import policy
import requests
from typing import List, Union, BinaryIO

# --- Third-party libraries ---
# Make sure you have installed the required libraries:
# pip install PyPDF2 python-docx langchain

try:
    from PyPDF2 import PdfReader
    from docx import Document
    from langchain.text_splitter import CharacterTextSplitter
except ImportError:
    print("Required libraries not found.")
    print("Please run: pip install PyPDF2 python-docx langchain")
    exit()

# ==============================================================================
# 1. CHUNKING FUNCTIONS
#    These functions extract text from different file types and split it.
# ==============================================================================

def getPdfChunks(file_obj: BinaryIO) -> List[str]:
    """Extracts text from a PDF file object and splits it into chunks."""
    text = ""
    try:
        # PyPDF2 can read directly from a file-like object
        pdf_reader = PdfReader(file_obj)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []

    if not text.strip():
        return []

    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return splitter.split_text(text)


def getDocxChunks(file_obj: BinaryIO) -> List[str]:
    """Extracts text from a DOCX file object and splits it into chunks."""
    full_text = []
    try:
        # python-docx can also read directly from a file-like object
        doc = Document(file_obj)
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return []

    if not full_text:
        return []
    
    text = "\n".join(full_text)
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return splitter.split_text(text)


def getEmailChunks(file_obj: BinaryIO) -> List[str]:
    """Extracts the plain text body from an email file object and chunks it."""
    text = ""
    try:
        # The email library reads from a binary file object
        msg = email.message_from_binary_file(file_obj, policy=policy.default)
        
        # Walk through email parts to find the plain text body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain' and part.get_payload(decode=True):
                    payload = part.get_payload(decode=True)
                    text += payload.decode('utf-8', errors='ignore')
        elif msg.get_content_type() == 'text/plain':
            payload = msg.get_payload(decode=True)
            if payload:
                text += payload.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error reading email: {e}")
        return []

    if not text.strip():
        return []

    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return splitter.split_text(text)


# ==============================================================================
# 2. HELPER FUNCTIONS
#    These functions download the file and identify its type.
# ==============================================================================




def getDocType(file_content: bytes) -> str:
    """
    Determines the document type by inspecting its first few bytes (magic numbers).
    """
    if file_content.startswith(b"%PDF"):
        return "pdf"
    if file_content.startswith(b"PK\x03\x04"): # ZIP file signature, used by DOCX
        # Further check to ensure it's a DOCX
        try:
            with zipfile.ZipFile(io.BytesIO(file_content)) as z:
                if "word/document.xml" in z.namelist():
                    return "docx"
        except zipfile.BadZipFile:
            pass # Not a valid zip file
    # A simple check for email headers. More robust checks are complex.
    if b"From:" in file_content[:1024] and b"Subject:" in file_content[:1024]:
        return "email"
    return "unknown"


# ==============================================================================
# 3. MAIN WORKFLOW FUNCTION
#    This function orchestrates the entire process.
# ==============================================================================

def chunker(file_obj: BinaryIO) -> List[str]:
    """
    Identifies a document's type from a file object and returns its text chunks.
    This function does NOT download. It only processes a given file object.
    """
    # Read the content to determine the file type
    file_obj.seek(0)
    content_for_detection = file_obj.read()
    file_obj.seek(0)  # Rewind so the chunking function can read it from the start

    # Get the document type
    doc_type = getDocType(content_for_detection)
    print(f"-> Detected document type: {doc_type}")

    # Call the appropriate chunker function
    chunks = []
    if doc_type == "pdf":
        chunks = getPdfChunks(file_obj)
    elif doc_type == "docx":
        chunks = getDocxChunks(file_obj)
    elif doc_type == "email":
        chunks = getEmailChunks(file_obj)
    else:
        print("-> Unsupported or unknown document type.")

    print(f"-> Found {len(chunks)} chunks.")
    return chunks
