from embedder import create_vectorstore
from rag_chain import generate_answer
from retriever import get_relevant_chunks
# import retriever
print(dir(retriever))

text = """
Diabetes is a chronic condition that affects how your body turns food into energy.
There are two main types: Type 1 and Type 2. Type 2 is more common and often linked to lifestyle.
"""

# Step 1: Embed the text and store vector index
create_vectorstore(text)

# Step 2: User question
question = "What are the types of diabetes?"

# Step 3: Retrieve relevant chunks
chunks = get_relevant_chunks(question)

# Step 4: Generate answer using GPT-4
answer = generate_answer(question, chunks)

print("Answer:", answer)