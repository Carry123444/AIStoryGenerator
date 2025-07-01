import streamlit as st
import google.generativeai as genai

# Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_story(prompt, model):
    response = model.generate_content(
        f"""Write a 200-word engaging story about: {prompt}
        Requirements:
        - 3 clear paragraphs
        - Vivid sensory details
        - Unexpected but satisfying ending""",
        generation_config={
            "max_output_tokens": 500,
            "temperature": 0.7
        }
    )
    return response.text

# Streamlit UI
st.set_page_config(page_title="Flash Story Generator")
st.title("✨ AI Story Generator(Using Gemini)")

prompt = st.text_area("Enter your story prompt:", placeholder="e.g., A detective solving a mystery...")

if st.button("✨ Generate Story"):
    with st.spinner("Crafting your story..."):
        story = generate_story(prompt, model)
        st.write(story)
        st.download_button("📥 Download", story)


st.markdown("---")
st.caption(f"Using {MODEL_NAME}")        
