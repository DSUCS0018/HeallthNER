import spacy
from spacy.tokens import DocBin
from spacy.scorer import Scorer
from spacy.training import Example

def load_test_data(spacy_test_file="bc5cdr_test.spacy"):
    doc_bin = DocBin().from_disk(spacy_test_file)
    nlp = spacy.blank("en")  # Blank model to get vocab
    return list(doc_bin.get_docs(nlp.vocab))

def get_entities(doc):
    return [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]

if __name__ == "__main__":
    # Load trained model
    model = spacy.load("healthner_model")

    # Load test data
    test_docs = load_test_data()

    examples = []

    for doc in test_docs:
        pred_doc = model(doc.text)
        example = Example(pred_doc, doc)
        examples.append(example)

    # Use Scorer to get metrics
    scorer = Scorer()
    scores = scorer.score(examples)

    print("📊 Evaluation Results:")
    print(f"Precision: {scores['ents_p']:.2f}")
    print(f"Recall:    {scores['ents_r']:.2f}")
    print(f"F1 Score:  {scores['ents_f']:.2f}")
