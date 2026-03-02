import os
import glob
import chromadb
from backend.config import settings
from backend.rag.embeddings import get_embedding

def load_and_chunk_markdown(file_path: str, chunk_size: int = 1000, overlap: int = 200) -> list[dict]:
    """Reads a markdown file and splits it into overlapping chunks."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to break at a newline if possible
        if end < text_length:
            last_newline = chunk.rfind('\n')
            if last_newline > chunk_size // 2:
                end = start + last_newline + 1
                chunk = text[start:end]
                
        chunks.append({
            "text": chunk.strip(),
            "source": os.path.basename(file_path),
            "start_idx": start,
            "end_idx": end
        })
        start = end - overlap

    return chunks

def init_knowledge_base():
    """Loads knowledge files, chunks them, generates embeddings, and saves to ChromaDB."""
    knowledge_dir = "knowledge"
    if not os.path.exists(knowledge_dir):
        print(f"Directory {knowledge_dir} not found. Skipping initialization.")
        return

    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
    
    # We create or get the collection
    collection = chroma_client.get_or_create_collection(name="scenario_knowledge")

    md_files = glob.glob(os.path.join(knowledge_dir, "*.md"))
    if not md_files:
        print("No markdown files found in knowledge directory.")
        return

    print(f"Found {len(md_files)} knowledge files. Processing...")

    all_chunks = []
    
    for file_path in md_files:
        print(f"Chunking {file_path}")
        chunks = load_and_chunk_markdown(file_path)
        all_chunks.extend(chunks)

    if not all_chunks:
        return

    # Process and add to Chroma in batches
    batch_size = 50
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        
        ids = []
        embeddings = []
        documents = []
        metadatas = []
        
        for j, chunk in enumerate(batch):
            chunk_id = f"{chunk['source']}_{chunk['start_idx']}_{chunk['end_idx']}"
            ids.append(chunk_id)
            documents.append(chunk['text'])
            metadatas.append({"source": chunk['source']})
            
            # Generate embedding
            print(f"Generating embedding for chunk {i+j}...")
            emb = get_embedding(chunk['text'])
            embeddings.append(emb)

        # Upsert into ChromaDB
        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Upserted batch of {len(batch)} chunks.")

    print("Knowledge base initialization complete!")

if __name__ == "__main__":
    init_knowledge_base()
