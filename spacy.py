import spacy

nlp = spacy.load("en_core_web_sm")

def process_resume_text(text):
    doc = nlp(text)

    # Tokenization
    tokens = [token.text for token in doc]
    print("Tokens:", tokens)

    # Named Entity Recognition (NER)
    for ent in doc.ents:
        print(ent.text, ent.label_)

    # Part-of-Speech Tagging
    for token in doc:
        print(token.text, token.pos_)

    # Lemmatization
    lemmas = [token.lemma_ for token in doc]
    print("Lemmas:", lemmas)