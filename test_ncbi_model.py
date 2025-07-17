import spacy

# Load your trained model
nlp = spacy.load("output/model-best")

# Try it on clinical-style text
text = "The patient was diagnosed with myocardial infarction and later developed Parkinson's disease."

doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)
