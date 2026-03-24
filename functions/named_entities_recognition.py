import spacy
nlp = spacy.load("en_core_web_sm")

def named_entities_recognition(book):    

    # Format book for use librairy
    doc = nlp(book)

    # Retrive person in the book
    persons = []
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.text not in persons:
            persons.append(ent.text)

    # Retrive location in the book
    locations = []
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"] and ent.text not in locations:
            locations.append(ent.text)
        
    return {
        "characters":persons,
        "locations":locations
    }


