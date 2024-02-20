import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json
from sklearn.model_selection import train_test_split
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity


nlp_vectoring = spacy.load("en_core_web_sm")
nlp = spacy.load("output/model-best")
db = DocBin()
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

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
    


def process_resumes(resume_json_strings, project):
    resume_evaluations = []
    for resume_json_str in resume_json_strings:
        # load json to get dictionary
        resume_dict = json.loads(resume_json_str)
        # extract text from dictionary
        resume_text = resume_dict["text"]
        # extract resume id for tracking
        resume_id = resume_dict["resume"]
        # entity recognition
        doc = nlp(resume_text)
        resume_features = extract_resume_info(doc)

        # entire resume checking for context
        #job_description_doc = nlp_vectoring(project["description"])
        #skills_doc = nlp_vectoring(project["skills"])
        #education_doc = nlp_vectoring(project["education"])

        resume_embedding = get_bert_embedding(resume_text)
        job_description_embedding = get_bert_embedding(project["description"])
        skills_embedding = get_bert_embedding(" ".join(project["skills"].split(', '))) 
        education_embedding = get_bert_embedding(project["education"])

        description_similarity = cosine_similarity(resume_embedding.detach().numpy(), job_description_embedding.detach().numpy())[0][0]
        skills_similarity = cosine_similarity(resume_embedding.detach().numpy(), skills_embedding.detach().numpy())[0][0]
        education_similarity = cosine_similarity(resume_embedding.detach().numpy(), education_embedding.detach().numpy())[0][0]

        score = score_resume(resume_features, project, description_similarity, skills_similarity, education_similarity)

        resume_evaluations.append({
            "resume_id": resume_id,
            "features": resume_features,
            "score": score
        })

    resume_evaluations.sort(key=lambda x: x['score'], reverse=True)

    return resume_evaluations

def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings

def score_resume(resume, project_info, description_similarity, skills_similarity, education_similarity):
        score = 0
    
        # Normalize and split skills from project_info
        required_skills = [skill.strip().lower() for skill in project_info["skills"].split(',')]
        print(f"Required skills: {required_skills}")

        # Normalize skills from resume
        resume_skills = [skill.strip().lower() for skill in resume['skills']]
        print(f"Resume skills: {resume_skills}")

        # Skills scoring with fuzzy matching
        for skill in required_skills:
            closest_matches = process.extract(skill, resume_skills, scorer=fuzz.partial_ratio, limit=1)
            if closest_matches:
                best_match, score_value = closest_matches[0]
                if score_value > 80:
                    print(f"Matched skill: {best_match} with a score of {score_value}")
                    score += 10

        # Education scoring
        for degree in resume['education']['degrees']:
            degree_normalized = degree.strip().lower()
            if any(fuzz.partial_ratio(degree_normalized, proj_ed.lower()) > 80 for proj_ed in project_info['education']):
                print(f"Matched education: {degree}")
                score += 5

        # Experience scoring
        project_years_list = [s for s in project_info["experience"].split() if s.isdigit()]
        if project_years_list:
            project_years = int(project_years_list[0])
            for experience_entry in resume['experience']['years of experience']:
                experience_entry_normalized = experience_entry.strip().lower()
                experience_years_list = [int(s) for s in experience_entry_normalized.split() if s.isdigit()]
                if experience_years_list and any(resume_year >= project_years for resume_year in experience_years_list):
                    print(f"Matched experience: {experience_entry}")
                    score += 5

        project_location_normalized = project_info["location"].strip().lower()
        resume_location_normalized = resume['personal_info']['location'].strip().lower()

        if fuzz.partial_ratio(project_location_normalized, resume_location_normalized) > 80:
            print(f"Matched location: {resume['personal_info']['location']}")
            score += 2

        score += description_similarity * 10  
        score += skills_similarity * 30       
        score += education_similarity * 20    


        return score

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