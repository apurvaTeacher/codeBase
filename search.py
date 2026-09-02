import chromadb
from chroma_store import get_collection
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

collection = get_collection()

def test_chroma_connection():

    count = collection.count()

    print("Connection to ChromaDB successful")
    print("Total chunks stored:", count)

test_chroma_connection()

def generate_query_embedding(query):

    embedding = model.encode(query)

    return embedding.tolist()

def search_documents(query, n_results=3):

    query_embedding = generate_query_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    formatted_results = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(documents)):

        formatted_results.append(
            {
                "text": documents[i],
                "filename": metadatas[i]["filename"],
                "page_number": metadatas[i]["page_number"],
                "distance": distances[i]
            }
        )

    return formatted_results

if __name__ == "__main__":

    results = search_documents(
        "when is room reserved for internal training?"
    )

    print(results)