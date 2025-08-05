from typing import List
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings  # ✅ updated import

embedder = OpenAIEmbeddings(model="text-embedding-3-small")

def get_relevant_chunks(query: str, index_path: str = "faiss_index") -> List[str]:
    db = FAISS.load_local(index_path, embeddings=embedder)
    docs = db.similarity_search(query, k=4)
    return [doc.page_content for doc in docs]