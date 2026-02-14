import os
import sys
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.loader import load_documents
from rag.chunking import split_documents
from rag.embeddings import get_embedding_model
from rag.vector_store import load_vector_store, create_vector_store
from rag.retriever import get_retriever
from rag.generator import generate_answer
from config.settings import FAISS_INDEX_PATH

def run_experiment():
    print("=========================================================")
    print("NIKE AI CONSULTANT - TEMPERATURE EXPERIMENT")
    print("=========================================================\n")

    # 1. Setup RAG components
    embed_model = get_embedding_model()
    
    # Ensure Vector Store exists
    if not os.path.exists(FAISS_INDEX_PATH):
        print("Initializing Vector Store for experiment...")
        docs = load_documents()
        chunks = split_documents(docs)
        vector_store = create_vector_store(chunks, embed_model)
    else:
        vector_store = load_vector_store(embed_model)
    
    retriever = get_retriever(vector_store)

    # Test Query
    query = "Can I work from a coffee shop?"

    # Case A Config
    config_a = {"temperature": 0.0, "top_p": 0.9}
    
    # Case B Config
    config_b = {"temperature": 0.8, "top_p": 0.95}

    print(f"Test Query: '{query}'\n")

    # -------------------------------------------------------
    # Run Case A
    # -------------------------------------------------------
    print(f"--- CASE A: Temp={config_a['temperature']}, Top_P={config_a['top_p']} ---")
    try:
        res_a = generate_answer(query, retriever, config_a['temperature'], config_a['top_p'])
        print("\n[Generated Response]:")
        print(res_a['result'])
    except Exception as e:
        print(f"Error in Case A: {e}")

    print("\n" + "="*50 + "\n")

    # -------------------------------------------------------
    # Run Case B
    # -------------------------------------------------------
    print(f"--- CASE B: Temp={config_b['temperature']}, Top_P={config_b['top_p']} ---")
    try:
        res_b = generate_answer(query, retriever, config_b['temperature'], config_b['top_p'])
        print("\n[Generated Response]:")
        print(res_b['result'])
    except Exception as e:
        print(f"Error in Case B: {e}")

    print("\n=========================================================")
    print("Experiment Complete. Check output for analysis.")

if __name__ == "__main__":
    load_dotenv()
    run_experiment()
