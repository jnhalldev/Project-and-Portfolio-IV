import spacy

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    # Normalize encoding to UTF-8, if not already
    # Replace newline characters with spaces (or remove them, if preferred)
    text = text.replace('\n', ' ')
    # Optionally, remove or replace other non-standard characters
    text = text.replace('Â', '')  # Example: removing 'Â'
    return text

def process_resumes(resume_texts):
    extracted_info = []
    for text in resume_texts:
        doc = nlp(text)
        # Example: Extract named entities
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        extracted_info.append({"entities": entities})
    return extracted_info
