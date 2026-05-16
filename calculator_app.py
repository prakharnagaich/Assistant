import streamlit as st

st.title("Simple Calculator")

num1 = st.number_input("Enter first number:", format="%.6f")
num2 = st.number_input("Enter second number:", format="%.6f")
operation = st.selectbox("Select operation:", ["Add", "Subtract", "Multiply", "Divide"])

def calculate(n1, n2, op):
    if op == "Add":
        return n1 + n2
    elif op == "Subtract":
        return n1 - n2
    elif op == "Multiply":
        return n1 * n2
    elif op == "Divide":
        if n2 == 0:
            return "Error: Division by zero"
        return n1 / n2

if st.button("Calculate"):
    result = calculate(num1, num2, operation)
    st.write("Result:", result)