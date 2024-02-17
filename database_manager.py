import zipfile
import fitz  # PyMuPDF
import json
from firebase_admin import storage
from account import GetUserIDToken
import requests
import account

def extract_text_from_pdf_stream(pdf_stream):
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def process_pdfs_in_zip(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        for filename in z.namelist():
            if filename.endswith(".pdf"):
                # Extract text from PDF
                with z.open(filename) as pdf_file:
                    pdf_bytes = pdf_file.read()
                    text = extract_text_from_pdf_stream(pdf_bytes)

                # Convert text to JSON
                json_data = json.dumps({"text": text}, ensure_ascii=False)
                
                # Upload JSON to Firebase Storage (or handle as needed)
                upload_json_to_storage(json_data, f"{filename}.json")

def upload_json_to_storage(json_data, destination_blob_name):
    bucket = storage.bucket()
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(json_data, content_type='application/json')
    print(f"Uploaded {destination_blob_name} to Firebase Storage")

def write_data_to_firebase(database_url, path, id_token, data):
    """Write data to a specified path in the Firebase Realtime Database."""
    url = f"{database_url}/{path}.json?auth={id_token}"
    response = requests.put(url, json=data)
    return response.json()