import spacy

def test_model(model_path="healthner_model"):
    # Load the saved model
    nlp = spacy.load(model_path)

    # Sample clinical texts to test
    texts = [
        "The patient was prescribed aspirin for heart disease.",
        "Aspirin is used to reduce fever and inflammation.",
        "Symptoms include headache and nausea.",
    ]

    for text in texts:
        doc = nlp(text)
        print(f"\nText: {text}")
        print("Entities:")
        for ent in doc.ents:
            print(f" - {ent.text} ({ent.label_})")

if __name__ == "__main__":
    test_model()
