import os, zipfile

def collect_documents(upload_path, temp_folder):

    os.makedirs(temp_folder, exist_ok=True)
    docs = []

    if upload_path.endswith(".docx"):
        docs.append((os.path.basename(upload_path), upload_path))

    elif upload_path.endswith(".zip"):

        extract_path = os.path.join(temp_folder, os.path.basename(upload_path)[:-4])
        zipfile.ZipFile(upload_path).extractall(extract_path)

        for root, _, files in os.walk(extract_path):
            for f in files:
                if f.endswith(".docx"):
                    docs.append((os.path.basename(upload_path), os.path.join(root, f)))

    return docs