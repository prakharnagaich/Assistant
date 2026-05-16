import streamlit as st

st.title("Binary to Words Converter")

binary_input = st.text_input("Enter binary string (e.g., 01001000 01100101 01101100 01101100 01101111):")

def binary_to_text(binary_str):
    try:
        # Split by spaces, convert each to a character
        chars = [chr(int(b, 2)) for b in binary_str.strip().split()]
        return ''.join(chars)
    except Exception:
        return "Invalid binary input!"

if binary_input:
    result = binary_to_text(binary_input)
    st.write("Output in words:", result)