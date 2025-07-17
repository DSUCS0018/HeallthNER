import spacy
from spacy.tokens import DocBin
from spacy import displacy

def visualize_entities(spacy_file="bc5cdr.spacy", output_file="output.html"):
    # Load the blank English model
    nlp = spacy.blank("en")

    # Load the .spacy dataset file
    doc_bin = DocBin().from_disk(spacy_file)
    docs = list(doc_bin.get_docs(nlp.vocab))

    # Get the first document
    doc = docs[0]

    # Define colors for different entity types
    colors = {
        "Chemical": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
        "Disease": "linear-gradient(90deg, #fca9a9, #fcd59c)"
    }
    options = {"ents": ["Chemical", "Disease"], "colors": colors}

    # Render entities with colors
    html = displacy.render(doc, style="ent", options=options)

    # Save the visualization to an HTML file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Saved visualization to {output_file}")

if __name__ == "__main__":
    visualize_entities()
