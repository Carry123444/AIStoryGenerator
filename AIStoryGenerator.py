import streamlit as st
try:
    import google.generativeai as genai
except ImportError:
    st.error("Missing packages! Add 'google-generativeai' to requirements.txt")
    st.stop()

GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")

def generate_story(prompt):
    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f"Write a 200-word story about: {prompt}\n"
            "- Include 3 paragraphs\n"
            "- Add sensory details\n"
            "- End with a twist"
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("✨ AI Story Generator (Gemini)")
prompt = st.text_input("Enter prompt:", "")

if st.button("Generate"):
    st.write(generate_story(prompt))
