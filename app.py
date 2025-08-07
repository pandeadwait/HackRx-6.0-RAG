from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import os
import io
import requests
import tempfile
from filereader import chunker
from embeddings import getEmbeddings
from rag_chain import generate_answer
from retriever import get_relevant_chunks
from typing import List, Union, BinaryIO

# class QueryRequest(BaseModel):
#     documents: str          
#     questions: List[str]    

# app = FastAPI()

# load_dotenv()
# bearer = os.environ.get('BEARER')

# def ingest_and_chunk_document(url: str):
#     doc = 
#     return chunker(doc)

# def find_relevant_info(question: str, chunks: List[str]):

#     print(f"Finding info for question: '{question}'")
#     return "This is the second chunk about grace periods."

# def generate_answer_from_info(question: str, relevant_info: str):
#     generate_answer()
#     return f"The answer to '{question}' is based on the grace period clause."
# # -----------------------------------------------------------

# @app.post("/api/v1/hackrx/run")
# async def run_submission(
#     req: QueryRequest,
#     authorization: Optional[str] = Header(None)
# ):
#     """
#     This function runs when a POST request is sent to your API.
#     """
#     # Step 1: Check the "password" (the Bearer token)
#     if authorization != "Bearer " + bearer:
#         raise HTTPException(status_code=401, detail="Incorrect or missing token")

#     # --- This is the Orchestration Logic ---
    
#     # Step 2: Get the document URL and chunk it (Person A's job)
#     all_text_chunks = ingest_and_chunk_document(req.documents)
    
#     final_answers = []
#     # Step 3: Loop through each question from the request
#     for question in req.questions:
#         # For each question, find the relevant info in the document (Person B's job)
#         relevant_info = find_relevant_info(question, all_text_chunks)
        
#         # Use that info to generate a final, human-readable answer (Person C's job)
#         final_answer = generate_answer_from_info(question, relevant_info)
        
#         # Add the answer to our list
#         final_answers.append(final_answer)

#     # Step 4: Return the final list of answers in the required JSON format
#     return {"answers": final_answers}

load_dotenv()
bearer = os.environ.get("BEARER")
app = FastAPI()

# def download(url, save_as = "downloaded.pdf"):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(save_as, "wb") as f:
#             f.write(response.content)

#         return save_as

# def download(url):
#     response = requests.get(url)

#     # Create a temporary file to store the downloaded content
#     temp_file = tempfile.NamedTemporaryFile(delete=True)
#     temp_file.write(response.content)
#     temp_file.seek(0)  # Rewind to the start of the file
#     return temp_file


def download(url: str) -> Union[io.BytesIO, None]:
    """
    Downloads a file from a URL and returns it as an in-memory binary object.
    This avoids saving anything to disk.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        # Return the content wrapped in an in-memory bytes buffer
        return io.BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from {url}: {e}")
        return None
    
@app.post("/api/v1/hackrx/run")
async def main(request: Request):
    data = await request.json()
    
    document = data['documents']
    questions = data['questions']
    
    print(document)

    file = download(document)

    chunks = chunker(file)
    vectorStore = getEmbeddings(chunks)

    answers = []
    for question in questions:
        releventChunks = get_relevant_chunks(question, vectorStore)
        answers.append(generate_answer(question, releventChunks))
    
    print(answers)

    return {"You sent" : data}