import os
import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
from PyPDF2 import PdfReader
import asyncio

# --- Sentence Transformer RAG Specific Imports for Tab 5 ---
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Try to import whisper
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False


# -------------------- Helper Functions (Tabs 1-4) --------------------
def read_file(file):
    if file.type == "application/pdf":
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
    # Using gemini-pro for consistency with other tabs
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

# -------------------- RAG Helper Functions (Tab 5) --------------------

def chunk_text_for_rag(text, chunk_size=500, chunk_overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

@st.cache_resource
def load_embedding_model():
    # Cache the model so it doesn't reload on every run
    return SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks, question, model):
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    question_embedding = model.encode([question], convert_to_tensor=True)
    return chunk_embeddings.cpu().numpy(), question_embedding.cpu().numpy()

def retrieve_top_chunks(chunks, chunk_embeddings, question_embedding, top_k=3):
    similarities = cosine_similarity(question_embedding, chunk_embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]


# -------------------- Main App --------------------
def main():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    st.set_page_config(page_title="Q&A with Gemini", layout="wide")
    
    st.title("Document, Web, YouTube & Video Q&A with Gemini")
    with st.container():
        st.markdown("---")
        api_key = st.text_input("🔑 Enter your Google API Key:", type="password", help="Enter your Gemini API key to get started")
        st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Document Upload", "🌐 URL Input", "🎥 YouTube Q&A", "🎬 MP4 Upload", "🤖 RAG Q&A"])

    # --- Tabs 1-4 remain unchanged ---
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

    # -------------------- Tab 5: RAG Q&A (UPDATED) --------------------
    with tab5:
        st.subheader("Ask questions about your document using RAG")
        st.markdown("This tab uses a local sentence-transformer model to find the most relevant parts of your document and feeds them to Gemini.")
        
        rag_uploaded_file = st.file_uploader("Upload a document (.txt or .pdf)", type=["txt", "pdf"], key="rag_doc_upload")
        rag_question = st.text_input("Your question:", key="rag_question", placeholder="Ask something based on the document...")

        if st.button("Get RAG Answer", key="rag_answer_btn", use_container_width=True):
            if not api_key: st.error("⚠️ Please enter your Google API Key first."); return
            if not rag_uploaded_file: st.error("⚠️ Please upload a document."); return
            if not rag_question: st.error("⚠️ Please enter a question."); return

            with st.spinner("Processing document and generating RAG answer..."):
                try:
                    # 1. Read and chunk the document
                    doc_text = read_file(rag_uploaded_file)
                    chunks = chunk_text_for_rag(doc_text)
                    
                    # 2. Load embedding model
                    embedding_model = load_embedding_model()

                    # 3. Embed chunks and question
                    chunk_embeddings, question_embedding = embed_chunks(chunks, rag_question, embedding_model)
                    
                    # 4. Retrieve top chunks
                    top_chunks = retrieve_top_chunks(chunks, chunk_embeddings, question_embedding)
                    
                    # 5. Build prompt and get response
                    context = "\n\n---\n\n".join(top_chunks)
                    prompt = f"Based on the following context, please provide a detailed answer to the question.\n\nContext:\n{context}\n\nQuestion:\n{rag_question}\n\nAnswer:"
                    
                    answer = get_gemini_response(prompt, api_key)

                    st.success("✅ Answer generated!")
                    st.markdown("### Answer")
                    st.write(answer)
                    
                    with st.expander("Show retrieved context"):
                        st.write(context)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()