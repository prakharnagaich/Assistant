import streamlit as st
import google.generativeai as genai

# Optional parsers
try:
    import docx
except Exception:
    docx = None

try:
    import PyPDF2
except Exception:
    PyPDF2 = None

st.set_page_config(page_title="Gemini Q&A", page_icon="??")

st.title("?? Gemini Q&A App")
st.write("Upload a document and ask questions based on its content using Google Gemini")

# Sidebar for API Key
st.sidebar.header("?? Configuration")
api_key = st.sidebar.text_input(
    "Enter your Gemini API Key",
    type="password",
    help="Get it from Google AI Studio"
)

# File uploader
uploaded_file = st.file_uploader("?? Upload a document (txt, pdf, docx)", type=["txt", "pdf", "docx"])

# Question input
question = st.text_area(
    "?? Your Question about the uploaded document",
    placeholder="Ask anything about the uploaded document...",
    height=120
)


def _extract_text_from_file(uploaded) -> str:
    if uploaded is None:
        return ""
    name = uploaded.name.lower() if hasattr(uploaded, "name") else ""
    # TXT
    if name.endswith(".txt"):
        raw = uploaded.read()
        return raw.decode("utf-8", errors="replace")

    # DOCX
    if name.endswith(".docx"):
        if docx is None:
            raise RuntimeError("python-docx is required to read .docx files. Install with `pip install python-docx`.")
        uploaded.seek(0)
        document = docx.Document(uploaded)
        paragraphs = [p.text for p in document.paragraphs]
        return "\n".join(paragraphs)

    # PDF
    if name.endswith(".pdf"):
        if PyPDF2 is None:
            raise RuntimeError("PyPDF2 is required to read PDF files. Install with `pip install PyPDF2`.")
        uploaded.seek(0)
        reader = PyPDF2.PdfReader(uploaded)
        texts = []
        for page in reader.pages:
            try:
                texts.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join(texts)

    # Fallback
    uploaded.seek(0)
    raw = uploaded.read()
    try:
        return raw.decode("utf-8", errors="replace")
    except Exception:
        return str(raw)


# Button
ask_button = st.button("Ask Gemini")

if ask_button:
    if not api_key:
        st.error("Please enter your Gemini API key.")
    elif uploaded_file is None:
        st.error("Please upload a document.")
    elif not question.strip():
        st.error("Please enter a question about the uploaded document.")
    else:
        try:
            # extract text
            with st.spinner("Extracting document text..."):
                doc_text = _extract_text_from_file(uploaded_file)
                if not doc_text.strip():
                    st.error("Could not extract any text from the uploaded document.")
                    st.stop()

            # Prepare prompt combining document content and the user's question
            # Keep the document content truncated to avoid overly long prompts
            if len(doc_text) > 4000:
                doc_text = doc_text[:3000] + "\n\n... (truncated) ...\n\n" + doc_text[-1000:]

            combined_prompt = f"Document content:\n{doc_text}\n\nQuestion:\n{question}\n\nAnswer concisely based on the document."

            # Call Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(combined_prompt)

            st.subheader("?? Gemini Response")
            st.write(getattr(response, "text", str(response)))

        except Exception as e:
            st.error(f"Error: {str(e)}")
