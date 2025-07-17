# 🩺 HealthNER

HealthNER is a Natural Language Processing (NLP) project built using [spaCy](https://spacy.io/) to automatically extract meaningful medical entities such as **diseases**, **symptoms**, and **drugs** from unstructured clinical text. This allows healthcare data to be converted into a more structured and analyzable format.

---

## 🚀 Key Features

- 🔍 Extracts **Diseases**, **Symptoms**, and other entities from raw medical text
- 🧠 Trains a custom Named Entity Recognition (NER) model using the **NCBI Disease dataset**
- 📈 Evaluates model performance using Precision, Recall, and F1 Score
- 🖼️ Visualizes entities using spaCy's `displacy` and Streamlit UI
- 📦 Deployable as an interactive web app

---

## 📊 Screenshots

### 🧪 Evaluation Results
![Model Evaluation Screenshot](health-ner.png)

### 💻 Streamlit Interface

#### 📥 Input
![Input Screenshot](ui_input.png.png)

#### 📤 Output
![Output Screenshot](ui_output.png.png)

---

## 📂 Project Structure

```bash
.
├── convert_ncbi_to_spacy.py     # Converts NCBI dataset into spaCy format
├── train.py                     # Trains the NER model using spaCy
├── test_model.py                # Tests the model on simple input
├── test_model_on_data.py        # Tests on complex clinical paragraphs
├── streamlit_app.py             # Streamlit UI for real-time testing
├── visualize.py                 # Saves NER visualizations as HTML
├── output/                      # Trained model files
├── README.md                    # Project overview
