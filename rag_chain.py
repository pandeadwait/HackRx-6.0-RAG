# import os
# from typing import List
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_answer(question: str, context_chunks: List[str]) -> str:
#     context = "\n".join(context_chunks)
#     prompt = f"""You are an assistant. Answer the question using only the context below.

# Context:
# {context}

# Question: {question}
# Answer:"""

#     response = client.chat.completions.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.2
#     )
#     return response.choices[0].message.content.strip()

import os
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model (choose 'gemini-pro' for text)
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def generate_answer(question: str, context_chunks: List[str]) -> str:
    context = "\n".join(context_chunks)
    prompt = f"""You are an assistant. Answer the question using only the context below.

Context:
{context}

Question: {question}
Answer:"""

    response = model.generate_content(prompt)
    return response.text.strip()
