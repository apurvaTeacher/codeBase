import sqlite3
import os
from datetime import datetime


DATABASE_NAME = "documents.db"


def create_tables():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            original_filename TEXT,
            file_path TEXT,
            file_type TEXT,
            upload_date TEXT,
            processing_status TEXT,
            category TEXT,
            dates TEXT,
            emails TEXT,
            invoice_numbers TEXT,
            total_amounts TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT,
            page_number INTEGER,
            extracted_text TEXT,
            FOREIGN KEY (document_id) REFERENCES documents(document_id)
        )
    """)
    conn.commit()
    conn.close()


def save_document(
    document_id,
    original_filename,
    file_path,
    file_type,
    processing_status,
    category
):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    upload_date = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO documents (
            document_id,
            original_filename,
            file_path,
            file_type,
            upload_date,
            processing_status,
            category
        )
        VALUES (?, ?, ?, ?, ?, ?,?)
    """, (
        document_id,
        original_filename,
        file_path,
        file_type,
        upload_date,
        processing_status,
        category
    ))

    conn.commit()
    conn.close()

def save_document_pages(document_id, pages):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    for page in pages:

        cursor.execute("""
            INSERT INTO document_pages (
                document_id,
                page_number,
                extracted_text
            )
            VALUES (?, ?, ?)
        """, (
            document_id,
            page["page_number"],
            page["text"]
        ))

    conn.commit()
    conn.close()

def update_processing_status(document_id, status):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE documents
        SET processing_status = ?
        WHERE document_id = ?
    """, (
        status,
        document_id
    ))

    conn.commit()
    conn.close()

def get_all_documents():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            document_id,
            original_filename,
            file_path,
            file_type,
            upload_date,
            processing_status, 
            category
        FROM documents
    """)

    rows = cursor.fetchall()

    conn.close()

    documents = []

    for row in rows:
        documents.append({
            "document_id": row[0],
            "original_filename": row[1],
            "file_path": row[2],
            "file_type": row[3],
            "upload_date": row[4],
            "processing_status": row[5],
            "category": row[6]
        })

    return documents

def get_document_by_id(document_id):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Get document information
    cursor.execute("""
        SELECT
            document_id,
            original_filename,
            file_path,
            file_type,
            upload_date,
            processing_status, 
            category
        FROM documents
        WHERE document_id = ?
    """, (document_id,))

    document_row = cursor.fetchone()

    if document_row is None:
        conn.close()
        return None

    # Get pages for this document
    cursor.execute("""
        SELECT
            page_number,
            extracted_text
            FROM document_pages
            WHERE document_id = ?
            ORDER BY page_number
        """, (document_id,))

    page_rows = cursor.fetchall()

    conn.close()

    pages = []

    for row in page_rows:
        pages.append({
            "page_number": row[0],
            "text": row[1]
        })

    document = {
        "document_id": document_row[0],
        "original_filename": document_row[1],
        "file_path": document_row[2],
        "file_type": document_row[3],
        "upload_date": document_row[4],
        "processing_status": document_row[5],
        "category": document_row[6],
        "pages": pages
    }

    return document


def delete_document_by_id(document_id):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Get file path first
    cursor.execute("""
        SELECT file_path
        FROM documents
        WHERE document_id = ?
    """, (document_id,))

    document = cursor.fetchone()

    if document is None:
        conn.close()
        return False

    file_path = document[0]

    # Delete page records
    cursor.execute("""
        DELETE FROM document_pages
        WHERE document_id = ?
    """, (document_id,))

    # Delete document record
    cursor.execute("""
        DELETE FROM documents
        WHERE document_id = ?
    """, (document_id,))

    conn.commit()
    conn.close()

    # Delete actual uploaded file
    if os.path.exists(file_path):
        os.remove(file_path)

    return True

def update_document_metadata(
    document_id,
    category,
    dates,
    emails,
    invoice_numbers,
    total_amounts
):
    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE documents
        SET category = ?,
            dates = ?,
            emails = ?,
            invoice_numbers = ?,
            total_amounts = ?
        WHERE document_id = ?
    """, (
        category,
        str(dates),
        str(emails),
        str(invoice_numbers),
        str(total_amounts),
        document_id
    ))

    conn.commit()
    conn.close()

def get_document_metadata_for_test(document_id):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            document_id,
            category,
            dates,
            emails,
            invoice_numbers,
            total_amounts
        FROM documents
        WHERE document_id = ?
    """, (document_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "document_id": row[0],
        "category": row[1],
        "dates": row[2],
        "emails": row[3],
        "invoice_numbers": row[4],
        "total_amounts": row[5]
    }