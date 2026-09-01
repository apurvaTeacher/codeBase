import os
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

# Maximum file size = 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024

UPLOAD_FOLDER = "uploads"
def folder_setup():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)