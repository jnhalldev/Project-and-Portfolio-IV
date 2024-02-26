import zipfile
import os
import fitz
import json
from firebase_admin import storage
import requests
from urllib3.exceptions import InsecureRequestWarning
from io import BytesIO
import pyrebase
import account

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
config = {
    "apiKey": "AIzaSyCQmi-nmvKtIE304cvwdqZEJrWy0LZIF4I",
    "authDomain": "resu-hunter.firebaseapp.com",
    "databaseURL": "https://resu-hunter-default-rtdb.firebaseio.com",
    "projectId": "resu-hunter",
    "storageBucket": "resu-hunter.appspot.com",
    "messagingSenderId": "369157629300",
    "appId": "1:369157629300:web:b4f00328f7a35643c2b821",
    "measurementId": "G-3YM8NJFZT2"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

def extract_text_from_pdf_stream(pdf_stream):
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    
    preprocessed_text = preprocess_text(text)

    return preprocessed_text

def preprocess_text(text):

    text = " ".join(text.split())
    text = text.replace('\n', ' ')
    text = text.replace('Â', '')
    
    return text

def process_pdfs_in_zip(database_url, path, id_token, zip_path, project_name):
    with zipfile.ZipFile(zip_path) as z:
        for filename in z.namelist():
            if filename.endswith(".pdf"):
                # Extract text from PDF
                with z.open(filename) as pdf_file:
                    pdf_bytes = pdf_file.read()
                    just_file_name = filename.split('/')[-1]
                    upload_pdf_to_database(project_name, pdf_bytes, just_file_name)
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

def upload_pdf_to_database(project_name, pdf, file_name):
    file_name = file_name.lstrip('/')
    path_on_cloud = f"{account.GetUserID()}/{project_name}/{file_name}"
    storage.child(path_on_cloud).put(pdf)

def upload_json_to_storage(database_url, path, id_token, data):
    url = f"{database_url}/{path}.json?auth={id_token}"
    response = requests.put(url, json=data, verify=False)
    print(f"Uploaded resume to Firebase Storage")

def write_data_to_firebase(database_url, path, id_token, data):
    """Write data to a specified path in the Firebase Realtime Database."""
    url = f"{database_url}/{path}.json?auth={id_token}"
    response = requests.put(url, json=data, verify=False)
    return response.json()

def download_file_from_firebase(file_list, storage_path, local_save_path):
    for resume in file_list[:5]:
        full_storage_path = f"{storage_path}{resume['resume_id']}.pdf"
        local_download_location = local_save_path
        print(full_storage_path)
        print(local_download_location)

        try:
            storage.child(full_storage_path).download(local_download_location,f"{resume['resume_id']}.pdf")
            print(f"File downloaded successfully and saved to {local_save_path}")
        except Exception as e:
            print(f"An error occurred while downloading the file: {e}")
