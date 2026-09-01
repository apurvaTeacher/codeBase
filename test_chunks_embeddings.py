from text_processing import chunk_pages
from embeddings import generate_embeddings


pages = [
    {
        "page_number": 1,
        "text": """
        ABC Technologies provides cloud infrastructure services.
        The company was founded in 2015.
        The head office is located in Pune.
        """
    },

    {
        "page_number": 2,
        "text": """
        The invoice total is 25000 rupees.
        Payment must be completed within 30 days.
        Late payment may result in additional charges.
        """
    }
]


chunks = chunk_pages(
    pages=pages,
    document_id="doc_101",
    filename="invoice.pdf",
    chunk_size=100,
    overlap=20
)


chunks_with_embeddings = generate_embeddings(chunks)


for chunk in chunks_with_embeddings:

    print("\n---------------------------")

    print("Document:", chunk["document_id"])
    print("Filename:", chunk["filename"])
    print("Page:", chunk["page_number"])
    print("Chunk:", chunk["chunk_number"])

    print("Text:")
    print(chunk["chunk_text"])

    print("Embedding length:")
    print(len(chunk["embedding"]))