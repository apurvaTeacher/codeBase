import fitz
import pytesseract
from PIL import Image
import os

def add_to_path():
     pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
     
def is_scanned_page(text):   
        return len(text) ==0


def convert_scanned_page_to_image(
    page,
    page_number,
    document_id
):

    # Folder for scanned PDF page images
    scanned_folder = os.path.join(
        "uploads",
        "scanned_pages"
    )

    os.makedirs(
        scanned_folder,
        exist_ok=True
    )

    # Create image filename
    image_filename = (
        f"{document_id}_page_{page_number}.png"
    )

    # Create image path
    image_path = os.path.join(
        scanned_folder,
        image_filename
    )

    # Convert PDF page to image
    pix = page.get_pixmap()

    # Save image
    pix.save(image_path)

    return image_path

def extract_pdf_text(
    file_path,
    document_id
):

    pages = []

    pdf = fitz.open(file_path)

    for page_number, page in enumerate(
        pdf,
        start=1
    ):

        # Extract normal embedded text
        text = page.get_text().strip()

        # Check whether page is scanned
        scanned = is_scanned_page(text)

        image_path = None
        extraction_method = "pymupdf"

        # Convert scanned page to image
        if scanned:

            image_path = (
                convert_scanned_page_to_image(
                    page,
                    page_number,
                    document_id
                )
            )
            image = Image.open(image_path)

            text = pytesseract.image_to_string(
                image
            ).strip()
            extraction_method = "tesseract"

        pages.append({
            "page_number": page_number,
            "text": text,
            "is_scanned": scanned,
            "extraction_method": extraction_method,
            "image_path": image_path
        })

    pdf.close()

    return pages



def extract_image_text(file_path):

    image = Image.open(file_path)

    text = pytesseract.image_to_string(image)

    pages = [
        {
            "page_number": 1,
            "text": text,
            "extraction_method": "tesseract",
            "is_scanned": True
        }
    ]

    return pages

