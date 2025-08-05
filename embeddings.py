import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

def getEmbeddings(texts):
    load_dotenv()
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(texts, embeddings)

    INDEX_PATH = "faissStore"

    vector_store.save_local(INDEX_PATH)
    
    return INDEX_PATH

#test
if __name__ == "__main__":
    texts = [
    "The Gemini family of models are the most capable and general models Google has ever built.",
    "FAISS is a library for efficient similarity search and clustering of dense vectors.",
    "LangChain is a framework for developing applications powered by language models.",
    "Embeddings create a vector representation of a piece of text.",
    "The quick brown fox jumps over the lazy dog.",
    "Storing text embeddings in a vector store allows for fast retrieval of similar documents."
    ]
    
    print(getEmbeddings(texts))
