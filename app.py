import streamlit as st
import os

from src.input_handler import collect_documents
from src.parser import get_document_info
from src.excel_writer import write_excel


UPLOAD_FOLDER = "uploads"
DOCS = "Documents"
OUTPUT_FILE = "output/results.xlsx"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("output", exist_ok=True)

st.title("GREG - Document Analyzer")

uploaded_file = st.file_uploader(
    "Upload a ZIP or DOCX file",
    type=["zip", "docx"]
)

if uploaded_file:

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded!")

    docs = collect_documents(file_path, DOCS)

    results = []

    for parent, path in docs:
        results.append(get_document_info(parent, path))

    write_excel(results, OUTPUT_FILE)

    st.subheader("Results")

    st.dataframe(results)

    with open(OUTPUT_FILE, "rb") as f:
        st.download_button(
            "Download Excel",
            f,
            file_name="results.xlsx"
        )