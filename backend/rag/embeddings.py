from google import genai
from backend.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Using the recommended embedding model
EMBEDDING_MODEL = "gemini-embedding-001"

def get_embedding(text: str) -> list[float]:
    """Generates an embedding for a given text using Gemini."""
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=genai.types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    return response.embeddings[0].values

def get_query_embedding(text: str) -> list[float]:
    """Generates an embedding for a query (with specific task_type)."""
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=genai.types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
    )
    return response.embeddings[0].values
