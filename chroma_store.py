import chromadb


client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="document_chunks"
)


def get_collection():
    return collection