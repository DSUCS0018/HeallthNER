from datasets import load_dataset
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

# Load NCBI Disease dataset
dataset = load_dataset("ncbi_disease", trust_remote_code=True)

# Define NER label map
label_map = {0: "O", 1: "B-Disease", 2: "I-Disease"}

# Load a blank English model
nlp = spacy.blank("en")

# Convert a split to spaCy format
def convert_to_spacy_format(split, output_path):
    doc_bin = DocBin()

    for example in tqdm(split):
        tokens = example["tokens"]
        tags = example["ner_tags"]
        doc = nlp.make_doc(" ".join(tokens))

        ents = []
        start = 0
        for token, tag in zip(tokens, tags):
            token_start = doc.text.find(token, start)
            token_end = token_start + len(token)
            start = token_end

            if tag == 1:  # B-Disease
                entity_start = token_start
                entity_end = token_end
            elif tag == 2:  # I-Disease
                entity_end = token_end
            else:
                if 'entity_start' in locals() and entity_end > entity_start:
                    span = doc.char_span(entity_start, entity_end, label="Disease")
                    if span:
                        ents.append(span)
                    del entity_start, entity_end

        # Catch last entity if not closed
        if 'entity_start' in locals() and entity_end > entity_start:
            span = doc.char_span(entity_start, entity_end, label="Disease")
            if span:
                ents.append(span)
            del entity_start, entity_end

        doc.ents = ents
        doc_bin.add(doc)

    doc_bin.to_disk(output_path)
    print(f"Saved {output_path}")

# Convert train, validation, and test splits
convert_to_spacy_format(dataset["train"], "ncbi_train.spacy")
convert_to_spacy_format(dataset["validation"], "ncbi_valid.spacy")
convert_to_spacy_format(dataset["test"], "ncbi_test.spacy")
