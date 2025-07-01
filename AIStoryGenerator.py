import streamlit as st
import google.generativeai as genai

# 1. Get free API key: https://ai.google.dev/
genai.configure(api_key="AIzaSyD3uUjIem0llLUwcs0qybigPdU3nyFrLpA")

def generate_story(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        f"Write a 200-word engaging story about: {prompt}\n"
        "- Include 3 paragraphs\n"
        "- Add sensory details\n"
        "- End with a twist"
    )
    return response.text

# Streamlit UI
st.title("✨ AI Story Generator (Gemini)")
prompt = st.text_input("Enter your prompt:", "")

if st.button("Generate"):
    st.write(generate_story(prompt))
