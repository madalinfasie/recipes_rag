import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings


class Settings:
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "google_genai")
    EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "models/gemini-embedding-001")

    MONGODB_CONN = os.environ["MONGODB_CONN"]
    QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")

    EMBEDDINGS = GoogleGenerativeAIEmbeddings(model=EMBEDDINGS_MODEL)
