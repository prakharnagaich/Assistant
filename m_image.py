import streamlit as st

# Try to import the official Google generative AI client and handle if it's not installed.
try:
    import google.generativeai as genai
except Exception:
    genai = None

# Optional OCR
try:
    from PIL import Image
    import pytesseract
except Exception:
    Image = None
    pytesseract = None

st.set_page_config(page_title="Gemini Image Q&A", page_icon="???")
st.title("??? Gemini Image Q&A")
st.write("Upload an image, optionally provide a short description, ask a question about the image, and get an answer from Gemini.")

# Sidebar for API Key
st.sidebar.header("?? Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")
MODEL_NAME = st.sidebar.text_input("Model name", value="gemini-2.5-flash")

# Image uploader
uploaded_image = st.file_uploader("Upload an image (png/jpg/jpeg)", type=["png", "jpg", "jpeg"])

# Optional user-provided description
image_description = st.text_input("Optional: brief description of the image (if OCR not available)")

# Question about the image
question = st.text_area("Question about the image", height=120)


def _extract_text_from_image(uploaded) -> str:
    if uploaded is None:
        return ""
    if Image is None or pytesseract is None:
        return ""
    try:
        uploaded.seek(0)
        img = Image.open(uploaded).convert('RGB')
        text = pytesseract.image_to_string(img)
        return text or ""
    except Exception:
        return ""


def _call_gemini(model_name: str, prompt: str, api_key: str) -> str:
    if genai is None:
        raise RuntimeError("`google-generativeai` package is not installed. Install with `pip install google-generativeai`.")
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel(model_name)
        resp = model.generate_content(prompt)
        return getattr(resp, 'text', str(resp))
    except Exception:
        # fallback to genai.generate
        resp = genai.generate(model=model_name, prompt=prompt)
        if isinstance(resp, dict):
            if 'candidates' in resp and resp['candidates']:
                return resp['candidates'][0].get('content') or str(resp)
        return str(resp)


if st.button("Ask about image"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif uploaded_image is None and not image_description.strip():
        st.error("Please upload an image or provide a brief description of it.")
    elif not question.strip():
        st.error("Please enter a question about the image.")
    else:
        # Build context
        ocr_text = _extract_text_from_image(uploaded_image)
        if ocr_text:
            context = f"Extracted text from image (OCR):\n{ocr_text}"
        elif image_description.strip():
            context = f"User-provided description of the image:\n{image_description.strip()}"
        else:
            context = "No image text or description available."

        # Prepare prompt
        combined_prompt = f"Image context:\n{context}\n\nQuestion:\n{question}\n\nAnswer based on the image. Be concise."

        try:
            answer = _call_gemini(MODEL_NAME, combined_prompt, api_key)
            st.subheader("?? Gemini Response")
            st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")
