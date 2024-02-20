import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json
from sklearn.model_selection import train_test_split
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


#nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("output/model-best")
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
    


def process_resumes(resume_json_strings, project):
    resume_evaluations = []
    for resume_json_str in resume_json_strings:
        resume_dict = json.loads(resume_json_str)
        resume_text = resume_dict["text"]
        resume_id = resume_dict["resume"]
        text = preprocess_text(resume_text)
        doc = nlp(text)
        resume_features = extract_resume_info(doc)
        score = score_resume(resume_features, project)
        resume_evaluations.append({
            "resume_id": resume_id,
            "features": resume_features,
            "score": score
        })

    resume_evaluations.sort(key=lambda x: x['score'], reverse=True)

    return resume_evaluations

def score_resume(resume, project_info):
        score = 0
    
        # Normalize and split skills from project_info
        required_skills = [skill.strip().lower() for skill in project_info["skills"].split(',')]
        print(f"Required skills: {required_skills}")

        # Normalize skills from resume
        resume_skills = [skill.strip().lower() for skill in resume['skills']]
        print(f"Resume skills: {resume_skills}")

        # Skills scoring with fuzzy matching
        for skill in required_skills:
            # Use the process.extract function to find the closest match to each required skill
            closest_matches = process.extract(skill, resume_skills, scorer=fuzz.partial_ratio, limit=1)
            if closest_matches:
                best_match, score_value = closest_matches[0]
                if score_value > 80:  # You can set your own threshold for what you consider a 'match'
                    print(f"Matched skill: {best_match} with a score of {score_value}")
                    score += 10

        # Skills scoring
        #required_skills = project_info["skills"].split(', ') 
        #resume_skills = resume['skills']
        #score += sum(10 for skill in required_skills if skill.lower() in [r_skill.lower() for r_skill in resume_skills])

        # Education scoring
        if any(project_info["education"].lower() in degree.lower() for degree in resume['education']['degrees']):
            score += 5

        # Experience scoring
        project_years_list = [s for s in project_info["experience"].split() if s.isdigit()]
        if project_years_list:  # Check if the list is not empty
            project_years = int(project_years_list[0])
            resume_years_list = [int(s) for degree in resume['experience']['years of experience'] for s in degree.split() if s.isdigit()]
            if any(resume_year >= project_years for resume_year in resume_years_list):
                score += 5

        if project_info["location"].lower() == resume['personal_info']['location'].lower():
            score += 2

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