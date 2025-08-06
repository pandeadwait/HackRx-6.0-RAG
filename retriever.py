from typing import List
from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings  # ✅ updated import
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embedder = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")

def get_relevant_chunks(query: str, index_path: str = "faiss_index") -> List[str]:
    db = FAISS.load_local(index_path, embeddings=embedder, allow_dangerous_deserialization = True)
    docs = db.similarity_search(query, k=4)
    
    return [doc.page_content for doc in docs]