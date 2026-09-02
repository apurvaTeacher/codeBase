def chunk_text(
    text,
    document_id,
    filename,
    page_number,
    chunk_size=500,
    overlap=50
):

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    start = 0
    chunk_number = 1

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:

            chunks.append({
                "document_id": document_id,
                "filename": filename,
                "page_number": page_number,
                "chunk_number": chunk_number,
                "chunk_text": chunk
            })

            chunk_number += 1

        start = end - overlap

    return chunks

def chunk_pages(
    pages,
    document_id,
    filename,
    chunk_size=500,
    overlap=50
):

    all_chunks = []

    for page in pages:

        page_number = page["page_number"]
        text = page["text"]

        page_chunks = chunk_text(
            text=text,
            document_id=document_id,
            filename=filename,
            page_number=page_number,
            chunk_size=chunk_size,
            overlap=overlap
        )

        all_chunks.extend(page_chunks)

    return all_chunks