from docx import Document
import os

def get_document_info(parent_file, file_path):

    doc = Document(file_path)

    word_count = 0

    for para in doc.paragraphs:
        word_count += len(para.text.split())

    pages = max(1, round(word_count / 300))

    return {
        "File": parent_file,
        "Name of Document": os.path.basename(file_path),
        "No. of Pages": pages
    }