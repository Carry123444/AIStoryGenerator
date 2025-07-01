import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# Configuration - No Hugging Face required
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY") or st.text_input("Enter Gemini API Key", type="password")
MODEL_NAME = "gemini-2.0-flash"  # Fastest free model

def setup_model():
    try:
        genai.configure(api_key=GEMINI_KEY)
        return genai.GenerativeModel(MODEL_NAME)
    except Exception as e:
        st.error(f"Model setup failed: {str(e)}")
        return None

def generate_story(prompt, model):
    try:
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
    except exceptions.InvalidArgument as e:
        return f"API Error: Check your API key"
    except Exception as e:
        return f"Generation failed: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Flash Story Generator")
st.title("📖 Gemini Flash Story Generator")

if not GEMINI_KEY:
    st.warning("Get a free API key from [Google AI Studio](https://aistudio.google.com/)")
else:
    model = setup_model()
    prompt = st.text_area("Your story prompt:", "A dragon who hates fire")
    
    if model and st.button("✨ Generate Story"):
        with st.spinner("Creating..."):
            story = generate_story(prompt, model)
            if story and not story.startswith(("API Error", "Generation failed")):
                st.subheader("Your Story")
                st.write(story)
                st.download_button("📥 Download", story)
            else:
                st.error(story)

# Footer
st.markdown("---")
st.caption(f"Using {MODEL_NAME} | Free tier limits apply")
