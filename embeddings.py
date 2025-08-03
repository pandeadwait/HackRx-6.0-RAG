import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# --- 1. Setup Environment ---
# Load environment variables from a .env file.
# Create a .env file in your project root and add the following line:
# GOOGLE_API_KEY="your_google_api_key"

def getEmbeddings(texts):
    load_dotenv()
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(texts, embeddings)

    INDEX_PATH = "faissStore"

    vector_store.save_local(INDEX_PATH)
    
    # # Now, let's load it back to prove it works.
    # # Note: You need to provide the same embedding function used to create the index.
    # print(f"\nLoading FAISS index from: {INDEX_PATH}")

    # # The allow_dangerous_deserialization flag is required for loading.
    # loaded_vector_store = FAISS.load_local(
    #     INDEX_PATH,
    #     embeddings,
    #     allow_dangerous_deserialization=True
    # )
    # print("Index loaded.")

    # # Test the loaded index with the same query
    # print("\nPerforming similarity search with the loaded index...")
    # try:
    #     loaded_docs = loaded_vector_store.similarity_search(query, k=2)
    #     print("\nSearch results from loaded index:")
    #     for i, doc in enumerate(loaded_docs):
    #         print(f"  {i+1}. Content: '{doc.page_content}'")
    # except Exception as e:
    #     print(f"Error during similarity search with loaded index: {e}")

    # # --- Required packages ---
    # # You need to install the following packages to run this script:
    # # pip install langchain langchain-google-genai faiss-cpu python-dotenv
    # #
    # # Note: Use 'faiss-gpu' instead of 'faiss-cpu' if you have a compatible NVIDIA GPU.
    return INDEX_PATH

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
    