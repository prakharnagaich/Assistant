
import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

def read_file(file):
    if file.type == "application/pdf":
        from PyPDF2 import PdfReader
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
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

def get_gemini_response(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

def main():
    st.set_page_config(page_title="Document & Web Q&A with Gemini", layout="wide")
    
    # Title and API Key section
    st.title("Document & Web Q&A with Gemini")
    with st.container():
        st.markdown("---")
        api_key = st.text_input("🔑 Enter your Google API Key:", type="password", help="Enter your Gemini API key to get started")
        st.markdown("---")

    # Tabs section
    tab1, tab2 = st.tabs(["📄 Document Upload", "🌐 URL Input"])

    with tab1:
        st.subheader("Ask questions about your document")
        col1, col2 = st.columns([2,1])
        with col1:
            uploaded_file = st.file_uploader("Upload a document (.txt or .pdf)", type=["txt", "pdf"], key="doc_upload")
        with col2:
            question_doc = st.text_input("Your question:", key="doc_question", placeholder="Ask about the document...")
        
        if st.button("Get Answer", key="doc_btn", use_container_width=True):
            if not api_key:
                st.error("⚠️ Please enter your Google API Key first.")
                return
            if not uploaded_file:
                st.error("⚠️ Please upload a document.")
                return
            if not question_doc:
                st.error("⚠️ Please enter a question.")
                return
            
            with st.spinner("Reading document and generating answer..."):
                doc_text = read_file(uploaded_file)
                prompt = f"Context:\n{doc_text}\n\nQuestion:\n{question_doc}\n\nAnswer:"
                response = get_gemini_response(prompt, api_key)
                st.success("Answer generated!")
                st.write(response)

    with tab2:
        st.subheader("Ask questions about a web page")
        col1, col2 = st.columns([2,1])
        with col1:
            url = st.text_input("Enter website URL:", key="url_input", placeholder="https://...")
        with col2:
            question_url = st.text_input("Your question:", key="url_question", placeholder="Ask about the webpage...")
        
        if st.button("Get Answer", key="url_btn", use_container_width=True):
            if not api_key:
                st.error("⚠️ Please enter your Google API Key first.")
                return
            if not url:
                st.error("⚠️ Please enter a URL.")
                return
            if not question_url:
                st.error("⚠️ Please enter a question.")
                return
            
            with st.spinner("Fetching webpage content and generating answer..."):
                doc_text = fetch_url_content(url)
                if doc_text.startswith("Error fetching URL:"):
                    st.error(doc_text)
                    return
                prompt = f"Context:\n{doc_text}\n\nQuestion:\n{question_url}\n\nAnswer:"
                response = get_gemini_response(prompt, api_key)
                st.success("Answer generated!")
                st.write(response)

if __name__ == "__main__":
    main()
