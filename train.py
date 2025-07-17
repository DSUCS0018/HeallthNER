import spacy
from spacy.tokens import DocBin
from spacy.training.example import Example
import random

def load_data(spacy_file):
    nlp = spacy.blank("en")
    doc_bin = DocBin().from_disk(spacy_file)
    docs = list(doc_bin.get_docs(nlp.vocab))
    examples = []
    for doc in docs:
        examples.append(Example.from_dict(doc, {"entities": [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]}))
    return examples

def main():
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")

    # Add entity labels
    labels = ["Chemical", "Disease"]
    for label in labels:
        ner.add_label(label)

    # Load training data
    train_examples = load_data("bc5cdr.spacy")

    # Begin training
    optimizer = nlp.begin_training()
    for i in range(20):  # number of iterations
        random.shuffle(train_examples)
        losses = {}
        for batch in spacy.util.minibatch(train_examples, size=8):
            nlp.update(batch, losses=losses, drop=0.2)
        print(f"Iteration {i + 1}, Losses: {losses}")

    # Save the model
    nlp.to_disk("healthner_model")
    print("Saved model to healthner_model")

if __name__ == "__main__":
    main()
