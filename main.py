from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import uuid
import docParser
import initialization
import classifier
from chunking import chunk_pages
from embeddings import generate_embeddings
from vector_database import store_chunks_in_chromadb,test_chromadb
from search import search_documents


from database import (
    create_tables,
    save_document,
    save_document_pages,
    update_processing_status,
    get_all_documents,
    get_document_by_id,
    delete_document_by_id,
    update_document_metadata,
    get_document_metadata_for_test
)

docParser.add_to_path()
initialization.folder_setup()
create_tables()

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Document Analyzer API is running"}

@app.get("/")
def home():
    return {"message": "Document Analyzer API"}

@app.get("/documents")
def get_documents():

    documents = get_all_documents()

    return {
        "documents": documents
    }

@app.get("/documents/{document_id}")
def get_document(document_id: str):

    document = get_document_by_id(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

@app.get("/test/metadata/{document_id}")
def test_document_metadata(document_id: str):

    metadata = get_document_metadata_for_test(document_id)

    if metadata is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return metadata

@app.get("/search")
def search(query: str):

    results = search_documents(query)

    return {
        "query": query,
        "results": results
    }

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):

    # 1. Validate file type
    extension = file.filename.split(".")[-1].lower()

    if extension not in initialization.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG and JPEG files are allowed"
        )

    # 2. Read file
    file_content = await file.read()

    # 3. Validate file size
    if len(file_content) > initialization.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 10 MB"
        )

    # 4. Generate unique document ID
    document_id = str(uuid.uuid4())

    # 5. Create unique filename
    saved_filename = f"{document_id}_{file.filename}"

    # 6. Create local file path
    file_path = os.path.join(
        initialization.UPLOAD_FOLDER,
        saved_filename
    )

    # 7. Save file locally
    with open(file_path, "wb") as saved_file:
        saved_file.write(file_content)

    

    # 8. Extract text from normal PDF
    pages = []

    if extension == "pdf":
        pages = docParser.extract_pdf_text(file_path,document_id)
              
    # Image OCR
    elif extension in {"png", "jpg", "jpeg"}:

        pages = docParser.extract_image_text(file_path)

    full_text = "\n".join(page["text"] for page in pages)
    # 9. Create chunks
    chunks = chunk_pages(
        pages,
        document_id,
        file.filename
    )

    category = classifier.classify_document(full_text)
    # emails = classifier.extract_email_addresses(full_text)
    # dates = classifier.extract_dates(full_text)
    # invoice_number = None

    # if category == "Invoice":
    #     invoice_number = classifier.extract_invoice_number(full_text)
    #     total_amount = classifier.extract_total_amount(full_text)

    save_document(
        document_id=document_id,
        original_filename=file.filename,
        file_path=file_path,
        file_type=extension,
        category = category,
        processing_status="uploaded"
        )
    metadata = classifier.extract_metadata(full_text,category)

    update_document_metadata(
        document_id,
        category,
        metadata["dates"],
        metadata["emails"],
        metadata["invoice_numbers"],
        metadata["total_amounts"]
    )
    save_document_pages(document_id, pages)
    update_processing_status(document_id,"processed")
    generate_embeddings(chunks)
    store_chunks_in_chromadb(chunks)
    test_chromadb()
   
    return {
        "document_id": document_id,
        "original_filename": file.filename,
        "saved_filename": saved_filename,
        "file_type": extension,
        "file_size": len(file_content),
        "file_path": file_path,
        "pages": pages,
        "catagory" : category,
        "message": "File uploaded and processed successfully"
    }

@app.delete("/documents/{document_id}")
def delete_document(document_id: str):

    deleted = delete_document_by_id(document_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "message": "Document deleted successfully"
    }