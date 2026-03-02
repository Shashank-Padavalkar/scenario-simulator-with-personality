import chromadb
from backend.config import settings
from backend.rag.embeddings import get_query_embedding

def retrieve_context(query: str, n_results: int = 3) -> list[str]:
    """Retrieves relevant text chunks from the vector database for a given query."""
    
    try:
        chroma_client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        collection = chroma_client.get_collection(name="scenario_knowledge")
    except Exception as e:
        print(f"Error accessing ChromaDB collection: {e}")
        return []
        
    query_embedding = get_query_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # Results is a dictionary with 'documents', 'metadatas', etc.
    if not results or 'documents' not in results or not results['documents']:
        return []
        
    # We only queried for one embedding, so we take the first item's documents
    documents = results['documents'][0]
    return documents
