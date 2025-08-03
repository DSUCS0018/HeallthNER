import streamlit as st
import spacy
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from io import BytesIO
import warnings

warnings.filterwarnings("ignore")

# -------------------- Page Config --------------------
st.set_page_config(page_title="HealthNER", layout="wide")


# -------------------- Load the model --------------------
@st.cache_resource
def load_model():
    try:
        # Try to load your custom model first
        return spacy.load("healthner_model")
    except OSError:
        # If custom model doesn't exist, try to download and load en_core_web_sm
        try:
            return spacy.load("en_core_web_sm")
        except OSError:
            # Download the model if it doesn't exist
            st.info("📥 Downloading spaCy English model... This may take a moment.")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            return spacy.load("en_core_web_sm")


nlp = load_model()

# -------------------- Sample Data --------------------
sample_texts = {
    "Example 1": "Famotidine is a histamine H2-receptor antagonist used to prevent ulcers.",
    "Example 2": "Indomethacin induced hypotension in sodium and volume depleted rats.",
    "Example 3": "Scleroderma renal crisis was caused by tacrolimus and prednisolone."
}

# -------------------- Dark Mode Toggle --------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode


st.sidebar.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode, on_change=toggle_dark_mode)

# -------------------- CSS Styling --------------------
base_css = """
    .highlight {
        padding: 2px 6px;
        border-radius: 4px;
        color: white;
        font-weight: bold;
    }
    .CHEMICAL { background: linear-gradient(to right, #00c6ff, #0072ff); }
    .DISEASE { background: linear-gradient(to right, #ff6a00, #ee0979); }
"""
dark_mode_css = """body, .stApp { background-color: #121212; color: #e0e0e0; }"""
light_mode_css = """body, .stApp { background-color: white; color: black; }"""

theme_css = dark_mode_css if st.session_state.dark_mode else light_mode_css
st.markdown(f"<style>{base_css}{theme_css}</style>", unsafe_allow_html=True)

# -------------------- Title --------------------
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
# st.image("medical.png", width=80)  # Commented out since image might not exist
st.markdown("<h1 style='margin-bottom: 0;'>🩺HealthNER</h1><p>Named Entity Recognition for Medical Text</p>",
            unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------- Session State --------------------
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "show_history" not in st.session_state:
    st.session_state.show_history = False

# -------------------- Sidebar History --------------------
with st.sidebar:
    if st.button("🕓 Show History"):
        st.session_state.show_history = not st.session_state.show_history

    if st.session_state.show_history and st.session_state.history:
        st.markdown("### Analyzed Texts:")
        for i, text in enumerate(st.session_state.history):
            st.markdown(f"**{i + 1}.** {text[:100]}...")

            try:
                doc = nlp(text)
                highlighted_text = text
                for ent in reversed(doc.ents):
                    label = f"[{ent.label_.upper()}]"
                    highlighted_text = (
                            highlighted_text[:ent.start_char] + label + ent.text + label + highlighted_text[
                                                                                           ent.end_char:]
                    )

                data = [(ent.text, ent.label_) for ent in doc.ents]
                df = pd.DataFrame(data, columns=["Entity", "Label"])

                # PDF Generation with proper error handling
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", style='B', size=16)
                    pdf.cell(0, 10, "HealthNER Analysis Report", ln=True, align='C')
                    pdf.set_font("Arial", size=12)

                    # Handle text encoding properly
                    safe_text = text.encode("latin-1", "replace").decode("latin-1")
                    safe_highlight = highlighted_text.encode("latin-1", "replace").decode("latin-1")

                    pdf.multi_cell(0, 10, f"\nOriginal Input:\n{safe_text}\n")
                    pdf.multi_cell(0, 10, f"\nNamed Entity Highlights:\n{safe_highlight}\n")

                    if not df.empty:
                        pdf.set_font("Arial", style='B', size=12)
                        pdf.cell(90, 10, "Entity", 1)
                        pdf.cell(90, 10, "Label", 1, ln=True)
                        pdf.set_font("Arial", size=12)
                        for row in data:
                            entity = row[0].encode("latin-1", "replace").decode("latin-1")
                            label = row[1].encode("latin-1", "replace").decode("latin-1")
                            pdf.cell(90, 10, entity, 1)
                            pdf.cell(90, 10, label, 1, ln=True)
                    else:
                        pdf.multi_cell(0, 10, "\nNo entities found.")

                    # Fixed PDF output handling
                    pdf_output = BytesIO()
                    pdf_bytes = pdf.output()
                    if isinstance(pdf_bytes, str):
                        pdf_output.write(pdf_bytes.encode('latin-1', 'replace'))
                    else:
                        pdf_output.write(pdf_bytes)
                    pdf_output.seek(0)

                    st.download_button(
                        label=f"⬇️ PDF {i + 1}",
                        data=pdf_output,
                        file_name=f"history_entry_{i + 1}.pdf",
                        mime="application/pdf"
                    )
                except Exception as pdf_error:
                    st.error(f"PDF generation failed: {str(pdf_error)}")

                # CSV download (this should work fine)
                if not df.empty:
                    csv_bytes = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"⬇️ CSV {i + 1}",
                        data=csv_bytes,
                        file_name=f"history_entry_{i + 1}.csv",
                        mime="text/csv"
                    )

            except Exception as e:
                st.error(f"Error processing history item {i + 1}: {str(e)}")

# -------------------- Load Sample --------------------
selected_example = st.selectbox("💡 Choose a sample text (optional)", ["-- Select --"] + list(sample_texts.keys()))
if selected_example != "-- Select --" and st.button("📥 Load Sample"):
    st.session_state.input_text = sample_texts[selected_example]
    st.rerun()

# -------------------- File Upload --------------------
uploaded_file = st.file_uploader("📄 Or upload a text file for analysis", type=["txt"])
if uploaded_file is not None:
    uploaded_text = uploaded_file.read().decode("utf-8")
    st.session_state.input_text = uploaded_text

# -------------------- Text Area --------------------
text_input = st.text_area("📝 Enter medical text below:", value=st.session_state.input_text, key="input_area",
                          height=200)

# -------------------- Analyze --------------------
if st.button("🔍 Analyze"):
    if text_input.strip():
        doc = nlp(text_input)
        st.session_state.history.append(text_input)

        html = text_input
        for ent in reversed(doc.ents):
            label = ent.label_.upper()
            span = f"<span class='highlight {label}'>{ent.text}</span>"
            html = html[:ent.start_char] + span + html[ent.end_char:]
        st.markdown(f"<div style='margin-top:20px'>{html}</div>", unsafe_allow_html=True)

        if doc.ents:
            data = [(ent.text, ent.label_) for ent in doc.ents]
            df = pd.DataFrame(data, columns=["Entity", "Label"])
            st.markdown("### 🧾 Extracted Entities")
            st.table(df)

            count_df = df['Label'].value_counts().reset_index()
            count_df.columns = ['Label', 'Count']

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📊 Bar Chart: Entity Frequency")
                fig_bar = px.bar(
                    count_df,
                    x='Label',
                    y='Count',
                    color='Label',
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    title="Entity Count"
                )
                fig_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)

            with col2:
                st.markdown("####  Pie Chart: Entity Distribution")
                fig_pie = px.pie(
                    count_df,
                    names='Label',
                    values='Count',
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    title='Entity Type Distribution'
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

        else:
            st.info("No entities found.")
    else:
        st.warning("Please enter some text to analyze.")

# -------------------- Clear --------------------
if st.button("🧹 Clear"):
    st.session_state.input_text = ""
    st.rerun()

