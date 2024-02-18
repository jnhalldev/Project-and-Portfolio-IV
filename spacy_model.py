import spacy

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    # Normalize encoding to UTF-8, if not already
    # Replace newline characters with spaces (or remove them, if preferred)
    text = text.replace('\n', ' ')
    text = text.replace('\\n', ' ')
    # Optionally, remove or replace other non-standard characters
    text = text.replace('Â', '')  # Example: removing 'Â'
    return text

def extract_resume_info(doc):
    # Example structure for storing extracted features
    resume_data = {
        "personal_info": {"name": "", "email": "", "phone": ""},
        "skills": [],
        "experience": [],
        "education": [],
        "certifications": [],
        "languages": []
    }

    for token in doc:
        if token.ent_type_ == "SKILL":
            resume_data["skills"].append(token.text)
        if token.ent_type_ == "SKILL":
            resume_data["skills"].append(token.text)

    return resume_data

def process_resumes(resume_texts):
    extracted_info = []
    for text in resume_texts:
        text = preprocess_text(text)
        doc = nlp(text)
        resume_features = extract_resume_info(doc)
        extracted_info.append(resume_features)
    return extracted_info
