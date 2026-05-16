import google.generativeai as genai

def generate_ai_explanation(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Explane AI in 100 words")
    print(response.text)

# Example usage:
api_key = "AIzaSyAHKPqEZ66TiHlG660ncBR-eIP-ehJo8OY"
generate_ai_explanation(api_key)