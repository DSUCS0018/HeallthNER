from datasets import load_dataset
from spacy.tokens import DocBin
import spacy

# Load dataset
dataset = load_dataset("bigbio/bc5cdr", name="bc5cdr_bigbio_kb", trust_remote_code=True, split="train")

# Initialize blank English model
nlp = spacy.blank("en")

def spans_overlap(span1, span2):
    # Returns True if two spans overlap
    return span1.start < span2.end and span2.start < span1.end

def convert_to_spacy_format(dataset, output_file="bc5cdr.spacy"):
    doc_bin = DocBin()
    skipped_entities = 0

    for i, example in enumerate(dataset):
        # Combine all sentences in all passages into one text string
        text = " ".join(" ".join(p['text']) for p in example["passages"])
        doc = nlp.make_doc(text)

        # Collect valid entity spans
        entities = []
        for ent in example["entities"]:
            for start, end in ent["offsets"]:
                span = doc.char_span(start, end, label=ent["type"])
                if span is not None:
                    entities.append(span)
                else:
                    skipped_entities += 1

        # Filter overlapping entities (keep longest spans)
        filtered_entities = []
        for span in sorted(entities, key=lambda x: x.end - x.start, reverse=True):
            if not any(spans_overlap(span, other) for other in filtered_entities):
                filtered_entities.append(span)

        doc.ents = filtered_entities
        doc_bin.add(doc)

        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1} examples...")

    doc_bin.to_disk(output_file)
    print(f"Saved to {output_file}. Skipped {skipped_entities} misaligned entities.")

if __name__ == "__main__":
    convert_to_spacy_format(dataset)
