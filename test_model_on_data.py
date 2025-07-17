import spacy

def test_model_on_examples():
    # Load your trained spaCy model
    nlp = spacy.load("healthner_model")

    # Example clinical texts to test
    texts = [
        "Famotidine-associated delirium. A series of six cases. Famotidine is a histamine H2-receptor antagonist used in inpatient settings for prevention of stress ulcers and is showing increasing popularity because of its low cost. Although all of the currently available H2-receptor antagonists have shown the propensity to cause delirium, only two previously reported cases have been associated with famotidine. The authors report on six cases of famotidine-associated delirium in hospitalized patients who cleared completely upon removal of famotidine. The pharmacokinetics of famotidine are reviewed, with no change in its metabolism in the elderly population seen. The implications of using famotidine in elderly persons are discussed.",
        "Indomethacin induced hypotension in sodium and volume depleted rats. After a single oral dose of 4 mg/kg indomethacin (IDM) to sodium and volume depleted rats plasma renin activity (PRA) and systolic blood pressure fell significantly within four hours. In sodium repleted animals indomethacin did not change systolic blood pressure (BP) although plasma renin activity was decreased. Thus, indomethacin by inhibition of prostaglandin synthesis may diminish the blood pressure maintaining effect of the stimulated renin-angiotensin system in sodium and volume depletion."
    ]

    # Run the model on each example and print the detected entities
    for i, text in enumerate(texts, start=1):
        doc = nlp(text)
        print(f"\nExample {i} Text:\n{text}\nEntities:")
        for ent in doc.ents:
            print(f" - {ent.text} ({ent.label_})")

if __name__ == "__main__":
    test_model_on_examples()
