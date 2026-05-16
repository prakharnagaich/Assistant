import streamlit as st
import fitz  # PyMuPDF
import docx
import tempfile
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# 🔐 Gemini API Key
GENAI_API_KEY = "AIzaSyAHKPqEZ66TiHlG660ncBR-eIP-ehJo8OY"  # Replace with your actual key
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# 🧠 Embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 🗂️ FAISS index
index = None
chunks_store = []

# 📄 Extract text from document
def extract_text(file):
    if file.name.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            doc = fitz.open(tmp.name)
            return " ".join([page.get_text() for page in doc])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    return ""

# 🔍 Chunk text
def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# 🧠 Embed and store in FAISS
def build_faiss_index(chunks):
    global index, chunks_store
    embeddings = embedder.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    chunks_store = chunks

# 🔎 Retrieve top-k chunks
def retrieve_chunks(query, k=3):
    query_vec = embedder.encode([query])
    D, I = index.search(np.array(query_vec), k)
    return [chunks_store[i] for i in I[0]]

# 🤖 Generate answer with Gemini
def generate_answer(context, query):
    prompt = f"""You are a helpful assistant. Use the following context to answer the question.

Context:
{context}

Question:
{query}
"""
    response = model.generate_content(prompt)
    return response.text

# 🎨 Streamlit UI
st.set_page_config(page_title="Gemini RAG with FAISS", layout="centered")
st.title("📄 Gemini RAG App (FAISS Edition)")
st.markdown("Upload a document and ask questions based on its content.")

uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
if uploaded_file:
    st.success("Document uploaded successfully!")
    text = extract_text(uploaded_file)
    chunks = chunk_text(text)
    build_faiss_index(chunks)
    st.info("Document processed and indexed.")

query = st.text_input("Ask a question based on the uploaded document")
if query and index:
    context = "\n".join(retrieve_chunks(query))
    answer = generate_answer(context, query)
    st.markdown("### 🤖 Gemini Response")
    st.write(answer)
elif query:
    st.warning("Please upload and process a document first.")