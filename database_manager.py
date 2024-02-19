import zipfile
import fitz
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
    
    preprocess_text = preprocess_text(text)

    return preprocess_text

def preprocess_text(text):

    text = " ".join(text.split())
    text = text.replace('\n', ' ')
    text = text.replace('Â', '')
    
    return text

def process_pdfs_in_zip(database_url, path, id_token, zip_path):
    with zipfile.ZipFile(zip_path) as z:
        for filename in z.namelist():
            if filename.endswith(".pdf"):
                # Extract text from PDF
                with z.open(filename) as pdf_file:
                    pdf_bytes = pdf_file.read()
                    text = extract_text_from_pdf_stream(pdf_bytes)
                
                parts = filename.split('/')
                resumeName = parts[-1]
                parts = resumeName.split('.')
                resumeName = parts[0]
                resumePath = f"{path}{resumeName}/"

                # Convert text to JSON
                json_data = json.dumps({"resume": resumeName,"text": text}, ensure_ascii=False)

                # Upload JSON to Firebase Storage (or handle as needed)
                upload_json_to_storage(database_url, resumePath, id_token, json_data)

def upload_json_to_storage(database_url, path, id_token, data):
    url = f"{database_url}/{path}.json?auth={id_token}"
    response = requests.put(url, json=data)
    print(f"Uploaded resume to Firebase Storage")

def write_data_to_firebase(database_url, path, id_token, data):
    """Write data to a specified path in the Firebase Realtime Database."""
    url = f"{database_url}/{path}.json?auth={id_token}"
    response = requests.put(url, json=data)
    return response.json()

#def fetch_resume_data():
#    placeholder = 2