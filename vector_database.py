import chromadb

from chroma_store import get_collection


def store_chunks_in_chromadb(chunks):

    collection = get_collection()

    for chunk in chunks:

        # Create a unique ID for every chunk
        chunk_id = (
            f"{chunk['document_id']}"
            f"_page_{chunk['page_number']}"
            f"_chunk_{chunk['chunk_number']}"
        )

        collection.upsert(
            ids=[chunk_id],

            documents=[
                chunk["chunk_text"]
            ],

            embeddings=[
                chunk["embedding"]
            ],

            metadatas=[
                {
                    "document_id": chunk["document_id"],
                    "filename": chunk["filename"],
                    "page_number": chunk["page_number"],
                    "chunk_number": chunk["chunk_number"]
                }
            ]
        )

    print("Chunks stored successfully in ChromaDB")

def test_chromadb():

    client = chromadb.PersistentClient(
        path="chroma_db"
    )

    collection = client.get_or_create_collection(
    name="document_chunks"
    )

    print("\n-----------------------------")
    print("CHROMADB TEST")
    print("-----------------------------")

    print("Total chunks stored:", collection.count())

    results = collection.get(
        limit=5,
        include=[
            "documents",
            "metadatas",
            "embeddings"
        ]
    )

    print("\nFirst few stored chunks:\n")

    for i in range(len(results["ids"])):

        print("Chunk ID:")
        print(results["ids"][i])

        print("\nText:")
        print(results["documents"][i])

        print("\nMetadata:")
        print(results["metadatas"][i])

        print("\nEmbedding length:")
        print(len(results["embeddings"][i]))

        print("\n-----------------------------")

if __name__ == "__main__":
    test_chromadb()