from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from settings import Settings

client = QdrantClient(Settings.QDRANT_HOST)


vector_size = len(Settings.EMBEDDINGS.embed_query("sample text"))

if not client.collection_exists("test"):
    client.create_collection(
        collection_name="test",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )

vector_store = QdrantVectorStore(
    client=client,
    collection_name="test",
    embedding=Settings.EMBEDDINGS,
)
