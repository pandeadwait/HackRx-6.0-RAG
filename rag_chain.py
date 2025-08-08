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
from google.generativeai import types
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

config = types.GenerationConfig(
    temperature=0.4
)
model = genai.GenerativeModel("gemini-2.5-flash", generation_config = config)

def generate_answer(question: str, context_chunks: List[str]) -> str:
    context = "\n".join(context_chunks)
    prompt = f"""You are an assistant. Answer the question using only the context below.

Context:
{context}

Question: {question}
Answer:"""

    response = model.generate_content(prompt)
    return response.text.strip()

# import os
# from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceEndpoint

# # Load environment variables from .env
# load_dotenv()

# repo_id = "Qwen/Qwen2.5-7B-Instruct-1M"

# # Initialize the HuggingFaceEndpoint with the model and your API token
# model = HuggingFaceEndpoint(
#     repo_id=repo_id,
#     temperature=0.5,
#     task = "conversational",
#     max_new_tokens=512
# )

# # Invoke the model
# response = model.invoke("Hello! Who are you?")
# print(response)

# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# API_URL = "https://router.huggingface.co/v1/chat/completions"
# headers = {
#     "Authorization": f"Bearer {os.environ['HUGGINGFACEHUB_API_TOKEN']}",
# }

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

# response = query({
#     "messages": [
#         {
#             "role": "user",
#             "content": "hello"
#         }
#     ],
#     "model": "Qwen/Qwen2.5-7B-Instruct-1M:featherless-ai"
# })

# print(response["choices"][0]["message"]["content"])