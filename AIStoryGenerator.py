import streamlit as st
import google.generativeai as genai

# Configure with your API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generate_story(prompt):
    try:
        # Use the correct model name
        model = genai.GenerativeModel('gemini-1.0-pro')
        response = model.generate_content(
            f"Write a 250-word story about: {prompt}\n"
            "Requirements:\n"
            "- 3 paragraphs\n"
            "- Vivid descriptions\n"
            "- Unexpected ending\n\n"
            "Story:"
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("✨ AI Story Generator")
prompt = st.text_area("Enter your story prompt:", "A girl who wants to be a singer")

if st.button("Generate Story"):
    with st.spinner("Creating your story..."):
        story = generate_story(prompt)
        st.write(story)
        st.download_button("Download Story", story, file_name="story.txt")

if st.button("Generate"):
    st.write(generate_story(prompt))
