import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json
from sklearn.model_selection import train_test_split


#nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("output\model-best")
db = DocBin()

def preprocess_text(text):
    text = text.replace('\n', ' ')
    text = text.replace('\\n', ' ')
    text = text.replace('Â', '')  # Example: removing 'Â'
    return text

def extract_resume_info(doc):
    # Updated structure for storing extracted features
        resume_data = {
            "personal_info": {
                "name": "",
                "email": "",
                "location": "",
            },
            "skills": [],
            "experience": {
                "positions": [],
                "companies": [],
                "years of experience": []
            },
            "education": {
                "degrees": [],
                "colleges": [],
                "certifications": [],
                "year of graduation": []
            },
            "links": []
        }

        for ent in doc.ents:
            # Print(ent.label_)  # Uncomment for debugging to see what entities are being recognized
            if ent.label_ == "NAME":
                resume_data["personal_info"]["name"] = ent.text
            elif ent.label_ == "EMAIL ADDRESS":
                resume_data["personal_info"]["email"] = ent.text
            elif ent.label_ == "LOCATION":
                resume_data["personal_info"]["location"] = ent.text
            elif ent.label_ == "SKILLS":
                resume_data["skills"].append(ent.text)
            elif ent.label_ == "WORKED AS":
                resume_data["experience"]["positions"].append(ent.text)
            elif ent.label_ == "DESIGNATIONS":
                resume_data["experience"]["positions"].append(ent.text)
            elif ent.label_ == "COMPANIES WORKED AT":
                resume_data["experience"]["companies"].append(ent.text)
            elif ent.label_ == "YEARS OF EXPERIENCE":
                resume_data["experience"]["years of experience"].append(ent.text)
            elif ent.label_ == "DEGREE":
                resume_data["education"]["degrees"].append(ent.text)
            elif ent.label_ == "COLLEGE NAME":
                resume_data["education"]["colleges"].append(ent.text)
            elif ent.label_ == "UNIVERSITY":
                resume_data["education"]["colleges"].append(ent.text)
            elif ent.label_ == "CERTIFICATION":
                resume_data["education"]["colleges"].append(ent.text)
            elif ent.label_ == "YEAR OF GRADUATION":
                resume_data["education"]["year of graduation"].append(ent.text)
            elif ent.label_ == "LINKED IN":
                resume_data["links"].append(ent.text)

        return resume_data
    


def process_resumes(resume_json_strings):
    extracted_info = []
    for resume_json_str in resume_json_strings:
        resume_dict = json.loads(resume_json_str)
        resume_text = resume_dict["text"]
        text = preprocess_text(resume_text)
        doc = nlp(text)
        resume_features = extract_resume_info(doc)
        extracted_info.append(resume_features)
    return extracted_info

def train_model():

    with open("data/training/dataset.json", "r") as file:
        resume_training_data = json.load(file)
        
    train, test = train_test_split(resume_training_data, test_size=0.3)
    
    for text,annot in tqdm(train):
        doc = nlp.make_doc(text)
        annot = annot['entities']
        ents = []
        entity_indices = []

        for start, end, label in annot:
            skip_entity = False
            for idx in range(start,end):
                if idx in entity_indices:
                    skip_entity = True
                    break
            if skip_entity== True:
                continue

            entity_indices = entity_indices + list(range(start,end))

            try:
                span = doc.char_span(start, end, label=label, alignment_mode='strict')
            except:
                continue

            if span is None:
                error_data = str([start, end]) + " " + str(text) + "\n"
                #file.write(error_data)

            else:
                ents.append(span)

    try:
        doc.ents = ents
        db.add(doc)
    except:
        pass

    db.to_disk('training_data.spacy')

    for text,annot in tqdm(test):
        doc = nlp.make_doc(text)
        annot = annot['entities']
        ents = []
        entity_indices = []

        for start, end, label in annot:
            skip_entity = False
            for idx in range(start,end):
                if idx in entity_indices:
                    skip_entity = True
                    break
            if skip_entity== True:
                continue

            entity_indices = entity_indices + list(range(start,end))

            try:
                span = doc.char_span(start, end, label=label, alignment_mode='strict')
            except:
                continue

            if span is None:
                error_data = str([start, end]) + " " + str(text) + "\n"
                #file.write(error_data)

            else:
                ents.append(span)

    try:
        doc.ents = ents
        db.add(doc)
    except:
        pass

    db.to_disk('test_data.spacy')

    file.close()