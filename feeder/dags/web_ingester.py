import datetime
import typing as t

from airflow.sdk import dag, task
from common.settings import Settings
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/134.0.0.0 Safari/537.36"
)


@dag(
    schedule=None,
    start_date=datetime.datetime(2021, 1, 1),
    catchup=False,
    tags=["web"],
)
def recipe_web_feeder():
    @task()
    def extract() -> list[dict]:
        # Load and chunk contents of the blog
        loader = RecursiveUrlLoader(
            "https://www.simplyrecipes.com/dinner-recipes-5091433",
            max_depth=1,
            prevent_outside=False,
        )

        # extractor (Optional[Callable[[str], str]]) – A function to extract document contents from raw HTML.
        # When extract function returns an empty string, the document is ignored. Default returns the raw HTML.

        return [m.model_dump() for m in loader.load()]

    @task
    def transform(serialized_docs: list[dict]) -> list[dict]:
        documents = [Document(**doc) for doc in serialized_docs]
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        all_splits = text_splitter.split_documents(documents)
        return [m.model_dump() for m in all_splits]

    @task()
    def load(serialized_splits: list[dict]):
        splits = [Document(**doc) for doc in serialized_splits]
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
        print(f"Loaded {len(splits)} documents\n{splits[0]}")
        vector_store.add_documents(documents=splits)

    documents = extract()
    splits = transform(documents)  # type: ignore
    load(splits)  # type: ignore


recipe_web_feeder()
