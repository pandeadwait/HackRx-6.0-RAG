from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import os

class QueryRequest(BaseModel):
    documents: str          
    questions: List[str]    

app = FastAPI()

load_dotenv()
bearer = os.environ.get('BEARER')

def ingest_and_chunk_document(url: str):
    print(f"Downloading and chunking document from: {url}")
    return ["This is the first chunk of the policy.", "This is the second chunk about grace periods.", "This is the final chunk."]

def find_relevant_info(question: str, chunks: List[str]):
    print(f"Finding info for question: '{question}'")
    return "This is the second chunk about grace periods."

def generate_answer_from_info(question: str, relevant_info: str):
    """
    (Person C's Job)
    Pretends to use an LLM (like GPT-4) to generate a final answer.
    """
    print(f"Generating answer using info: '{relevant_info}'")
    # In reality, this would make an API call to an LLM.
    return f"The answer to '{question}' is based on the grace period clause."
# -----------------------------------------------------------

@app.post("/api/v1/hackrx/run")
async def run_submission(
    req: QueryRequest,
    authorization: Optional[str] = Header(None)
):
    """
    This function runs when a POST request is sent to your API.
    """
    # Step 1: Check the "password" (the Bearer token)
    if authorization != "Bearer " + bearer:
        raise HTTPException(status_code=401, detail="Incorrect or missing token")

    # --- This is the Orchestration Logic ---
    
    # Step 2: Get the document URL and chunk it (Person A's job)
    all_text_chunks = ingest_and_chunk_document(req.documents)
    
    final_answers = []
    # Step 3: Loop through each question from the request
    for question in req.questions:
        # For each question, find the relevant info in the document (Person B's job)
        relevant_info = find_relevant_info(question, all_text_chunks)
        
        # Use that info to generate a final, human-readable answer (Person C's job)
        final_answer = generate_answer_from_info(question, relevant_info)
        
        # Add the answer to our list
        final_answers.append(final_answer)

    # Step 4: Return the final list of answers in the required JSON format
    return {"answers": final_answers}

