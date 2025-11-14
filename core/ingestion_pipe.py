from chonkie import Pipeline, AutoEmbeddings
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# Get the embeddings handler for SentenceTransformer
embeddings = AutoEmbeddings.get_embeddings("BAAI/bge-base-en-v1.5")

def ingest_data_to_store_with_fetch():
    # Process all markdown files in a directory
    (Pipeline()
     .fetch_from("file", dir="./documents", ext=[".md", ".txt"])
     .process_with("text")
     .chunk_with("recursive", chunk_size=512)
     .run())
    print(f"Ingested documents")


def ingest_data_to_store(text: str):
    print(f"Indexing in Qdrant store in collection: {os.environ.get('COLLECTION_NAME')}")
    (Pipeline()
     .process_with("text")
     .chunk_with("semantic", threshold=0.8)
     .refine_with("overlap", context_size=100)
     .store_in("qdrant",
               collection_name=os.environ.get('COLLECTION_NAME'),
               url=os.environ.get("QDRANT_URL"),
               api_key=os.environ.get("QDRANT_API_KEY"),
               embedding_model=embeddings)
     .run(texts=text))
    print(f"Ingested documents")
