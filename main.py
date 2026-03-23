from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import shutil
import os

from src.input_handler import collect_documents
from src.parser import get_document_info
from src.excel_writer import write_excel


UPLOAD_FOLDER = "uploads"
DOCS = "Documents"
OUTPUT_FILE = "output/results.xlsx"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOCS, exist_ok=True)
os.makedirs("output", exist_ok=True)


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = collect_documents(file_path, DOCS)

    results = []

    for parent, path in docs:
        results.append(get_document_info(parent, path))

    write_excel(results, OUTPUT_FILE)

    return {
        "results": results
    }


@app.get("/download")
def download():
    return FileResponse(
        OUTPUT_FILE,
        filename="results.xlsx"
    )