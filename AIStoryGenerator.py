import streamlit as st
import google.generativeai as genai

# 1. Get your free API key from https://aistudio.google.com/app/apikey
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY") 

# Initialize the model (using current working model names)
try:
    genai.configure(api_key=GEMINI_KEY)
    
    # Try both current model name formats
    try:
        model = genai.GenerativeModel('gemini-1.0-pro')  # Primary attempt
    except:
        model = genai.GenerativeModel('models/gemini-pro')  # Fallback format
except Exception as e:
    st.error(f"API setup failed: {str(e)}")
    st.stop()

def generate_story(prompt):
    try:
        response = model.generate_content(
            f"""Write a 250-word engaging story about: {prompt}
            Structure:
            1. Captivating opening
            2. Character development
            3. Satisfying conclusion
            
            Story must include:
            - Vivid descriptions
            - Emotional depth
            - One unexpected twist
            
            Story:""",
            generation_config={
                "max_output_tokens": 500,
                "temperature": 0.7
            }
        )
        return response.text
    except Exception as e:
        return f"⚠️ Generation failed. Error: {str(e)}"

# Streamlit UI
st.title(" AI Story Generator (Gemini)")
prompt = st.text_area("Enter your prompt:", "")

if st.button("✨ Generate Story"):
    with st.spinner("Creating your story..."):
        story = generate_story(prompt)
        st.subheader("Your Story")
        st.write(story)
        st.download_button("📥 Download", story, file_name="story.txt")

# Debug info
st.markdown("---")
st.caption(f"Using model: {model._model_name}")
