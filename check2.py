import os
import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

# --- New Imports for RAG Tab ---
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF
import docx

# Try to import whisper
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# -------------------- RAG Specific Initializations --------------------
# Using st.session_state to persist the index and chunks across reruns
if 'index' not in st.session_state:
    st.session_state.index = None
if 'chunks_store' not in st.session_state:
    st.session_state.chunks_store = []

# Initialize the embedding model once
@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedder = load_embedder()


# -------------------- Helper Functions --------------------
def read_file(file):
    if file.type == "application/pdf":
        from PyPDF2 import PdfReader
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        return file.read().decode("utf-8")


def fetch_url_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        texts = soup.stripped_strings
        return " ".join(texts)
    except Exception as e:
        return f"Error fetching URL: {e}"


def fetch_youtube_transcript(youtube_url):
       from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
       import re
       match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", youtube_url)
       if not match:
           return "Error: Could not extract video ID from URL."
       video_id = match.group(1)
       try:
           ytt_api = YouTubeTranscriptApi()
           out = []
           transcript_list = ytt_api.fetch(video_id, languages=['en'])
           for a in transcript_list:
               outtex = a.text  # Use attribute access instead of subscript
               out.append(outtex)
   # Join the list into a single string and remove commas and single quotes
               cleaned_output = " ".join(out).replace(",", "").replace("'", "")
           return cleaned_output
       except TranscriptsDisabled:
           return "Error: Transcripts are disabled for this video."
       except NoTranscriptFound:
           return "Error: No transcript found for this video."
       except Exception as e:
           return f"Error fetching transcript: {e}"


def video_to_transcript(video_path, language='en'):
    audio_path = 'temp_audio.wav'
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()

    audio = AudioSegment.from_wav(audio_path)
    audio = audio.set_channels(1)
    audio = audio.normalize()
    audio.export(audio_path, format="wav")

    transcript = ""
    if WHISPER_AVAILABLE:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language=language)
        transcript = result['text']
    else:
        recognizer = sr.Recognizer()
        chunk_length_ms = 60 * 1000
        chunks = [audio[i:i+chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
        for i, chunk in enumerate(chunks):
            chunk_filename = f"temp_chunk_{i}.wav"
            chunk.export(chunk_filename, format="wav")
            with sr.AudioFile(chunk_filename) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language=language)
                except sr.UnknownValueError:
                    text = "[Unintelligible]"
                except sr.RequestError as e:
                    text = f"[Error: {e}]"
            transcript += text + "\n"
            os.remove(chunk_filename)
    os.remove(audio_path)
    return transcript


def get_gemini_response(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


# -------------------- New Helper Functions for RAG Tab --------------------
def extract_text_rag(file):
    # Use a temporary file to handle the uploaded file object
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp:
        tmp.write(file.getvalue())
        tmp_path = tmp.name

    text = ""
    if file.name.endswith(".pdf"):
        doc = fitz.open(tmp_path)
        text = " ".join([page.get_text() for page in doc])
    elif file.name.endswith(".docx"):
        doc = docx.Document(tmp_path)
        text = " ".join([para.text for para in doc.paragraphs])

    os.remove(tmp_path)
    return text

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def build_faiss_index(chunks):
    embeddings = embedder.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    st.session_state.index = index
    st.session_state.chunks_store = chunks

def retrieve_chunks(query, k=3):
    query_vec = embedder.encode([query])
    D, I = st.session_state.index.search(np.array(query_vec).astype('float32'), k)
    return [st.session_state.chunks_store[i] for i in I[0]]

# -------------------- Main App --------------------
def main():
    st.set_page_config(page_title="Document, Web, YouTube & Video Q&A with Gemini", layout="wide")
    
    st.title("Document, Web, YouTube & Video Q&A with Gemini")
    with st.container():
        st.markdown("---")
        api_key = st.text_input("🔑 Enter your Google API Key:", type="password", help="Enter your Gemini API key to get started")
        st.markdown("---")

    # Added the 5th tab
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Document Upload", "🌐 URL Input", "🎥 YouTube Q&A", "🎬 MP4 Upload", "🧠 RAG Q&A"])

    # -------------------- Tab 1: Document --------------------
    with tab1:
        st.subheader("Ask questions about your document")
        col1, col2 = st.columns([2,1])
        with col1:
            uploaded_file = st.file_uploader("Upload a document (.txt or .pdf)", type=["txt", "pdf"], key="doc_upload")
        with col2:
            question_doc = st.text_input("Your question:", key="doc_question", placeholder="Ask about the document...")
        
        if st.button("Get Answer", key="doc_btn", use_container_width=True):
            if not api_key: st.error("⚠️ Please enter your Google API Key first."); return
            if not uploaded_file: st.error("⚠️ Please upload a document."); return
            if not question_doc: st.error("⚠️ Please enter a question."); return
            
            with st.spinner("Reading document and generating answer..."):
                doc_text = read_file(uploaded_file)
                prompt = f"Context:\n{doc_text}\n\nQuestion:\n{question_doc}\n\nAnswer:"
                response = get_gemini_response(prompt, api_key)
                st.success("Answer generated!")
                st.markdown(response)

    # -------------------- Tab 2: URL --------------------
    with tab2:
        st.subheader("Ask questions about a web page")
        col1, col2 = st.columns([2,1])
        with col1:
            url = st.text_input("Enter website URL:", key="url_input", placeholder="https://...")
        with col2:
            question_url = st.text_input("Your question:", key="url_question", placeholder="Ask about the webpage...")
        
        if st.button("Get Answer", key="url_btn", use_container_width=True):
            if not api_key: st.error("⚠️ Please enter your Google API Key first."); return
            if not url: st.error("⚠️ Please enter a URL."); return
            if not question_url: st.error("⚠️ Please enter a question."); return
            
            with st.spinner("Fetching webpage content and generating answer..."):
                doc_text = fetch_url_content(url)
                if doc_text.startswith("Error fetching URL:"): st.error(doc_text); return
                prompt = f"Context:\n{doc_text}\n\nQuestion:\n{question_url}\n\nAnswer:"
                response = get_gemini_response(prompt, api_key)
                st.success("Answer generated!")
                st.markdown(response)

    # -------------------- Tab 3: YouTube --------------------
    with tab3:
        st.subheader("Ask questions about a YouTube video")
        col1, col2 = st.columns([2,1])
        with col1:
            youtube_url = st.text_input("Enter YouTube video URL:", key="yt_url", placeholder="https://www.youtube.com/watch?v=...")
        with col2:
            question_yt = st.text_input("Your question:", key="yt_question", placeholder="Ask about the video transcript...")
        
        if st.button("Get Answer", key="yt_btn", use_container_width=True):
            if not api_key: st.error("⚠️ Please enter your Google API Key first."); return
            if not youtube_url: st.error("⚠️ Please enter a YouTube video URL."); return
            if not question_yt: st.error("⚠️ Please enter a question."); return
            
            with st.spinner("Fetching YouTube transcript and generating answer..."):
                transcript = fetch_youtube_transcript(youtube_url)
                if transcript.startswith("Error"): st.error(transcript); return
                prompt = f"Context:\n{transcript}\n\nQuestion:\n{question_yt}\n\nAnswer:"
                response = get_gemini_response(prompt, api_key)
                st.success("Answer generated!")
                st.markdown(response)

    # -------------------- Tab 4: MP4 Upload --------------------
    with tab4:
        st.subheader("Ask questions about an uploaded MP4 video")
        col1, col2 = st.columns([2,1])
        with col1:
            uploaded_video = st.file_uploader("Upload an MP4 video", type=["mp4"], key="video_upload")
            language = st.selectbox("Select language spoken in video", ["en", "hi", "es", "fr", "de", "zh", "ja"])
        with col2:
            question_video = st.text_input("Your question:", key="video_question", placeholder="Ask about the video transcript...")

        if st.button("Get Answer", key="video_btn", use_container_width=True):
            if not api_key: st.error("⚠️ Please enter your Google API Key first."); return
            if not uploaded_video: st.error("⚠️ Please upload an MP4 video."); return
            if not question_video: st.error("⚠️ Please enter a question."); return

            with st.spinner("Transcribing video and generating answer..."):
                temp_video_path = "temp_video.mp4"
                with open(temp_video_path, "wb") as f: f.write(uploaded_video.read())
                transcript = video_to_transcript(temp_video_path, language=language)
                os.remove(temp_video_path)

                prompt = f"Context:\n{transcript}\n\nQuestion:\n{question_video}\n\nAnswer:"
                response = get_gemini_response(prompt, api_key)
                st.success("Answer generated!")
                st.markdown(response)

    # -------------------- Tab 5: RAG Q&A --------------------
    with tab5:
        st.subheader("Ask context-aware questions using RAG")
        
        uploaded_file_rag = st.file_uploader("Upload a document (.pdf or .docx)", type=["pdf", "docx"], key="rag_upload")
        
        if uploaded_file_rag:
            with st.spinner("Processing and indexing document..."):
                text = extract_text_rag(uploaded_file_rag)
                chunks = chunk_text(text)
                build_faiss_index(chunks)
            st.success("Document processed and indexed successfully!")

        question_rag = st.text_input("Your question:", key="rag_question", placeholder="Ask about the indexed document...")

        if st.button("Get Answer", key="rag_btn", use_container_width=True):
            if not api_key: st.error("⚠️ Please enter your Google API Key first."); return
            if not uploaded_file_rag: st.error("⚠️ Please upload and process a document first."); return
            if not question_rag: st.error("⚠️ Please enter a question."); return
            if st.session_state.index is None: st.warning("Please upload and process a document first."); return
            
            with st.spinner("Retrieving context and generating answer..."):
                context = "\n---\n".join(retrieve_chunks(question_rag))
                prompt = f"""You are a helpful assistant. Use ONLY the following context to answer the question. If the answer is not in the context, say 'The answer is not available in the provided document.'

Context:
{context}

Question:
{question_rag}
"""
                response = get_gemini_response(prompt, api_key)
                st.success("Answer generated!")
                st.markdown("### 🤖 Gemini Response")
                st.markdown(response)


if __name__ == "__main__":
    main()