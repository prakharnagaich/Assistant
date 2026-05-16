# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        return f"Error fetching URL: {e}"

def ask_gemma(question, context):
    payload = {
        "model": "gemma3:4b",
        "prompt": f"Context:\n{context}\n\n. Based only from the context provide answer to this Question: {question}",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "No response")

st.title("Gemma3:4b Web Q&A")

url = st.text_input("Enter a URL")
question = st.text_input("Ask a question about the page")

if st.button("Submit"):
    with st.spinner("Processing..."):
        page_text = extract_text_from_url(url)
        answer = ask_gemma(question, page_text)
        st.subheader("Answer:")
        st.write(answer)