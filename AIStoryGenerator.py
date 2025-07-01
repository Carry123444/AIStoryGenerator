import streamlit as st
import google.generativeai as genai

# 1. Get your API key from https://aistudio.google.com/app/apikey
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY") 

# Initialize with the CORRECT model name
try:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-pro')  # The only working free tier name
except Exception as e:
    st.error(f"❌ Setup failed: {str(e)}")
    st.stop()

def generate_story(prompt):
    try:
        response = model.generate_content(
            f"""Write a 250-word story about: {prompt}
            
            Requirements:
            - 3 clear paragraphs
            - Vivid descriptions
            - Unexpected ending
            
            Story:""",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=500,
                temperature=0.7
            )
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}\n\nTry again in 60 seconds (free tier limit)"

# Streamlit UI
st.title("✨ AI Story Generator (Gemini)")
prompt = st.text_area("Prompt:", "A girl who wants to be a singer")

if st.button("Generate"):
    with st.spinner("Writing..."):
        story = generate_story(prompt)
        if not story.startswith("⚠️"):
            st.success("✅ Story generated!")
            st.write(story)
            st.download_button("Download", story)
        else:
            st.error(story)

# Debug info
st.markdown("---")
st.caption("Using model: gemini-pro (free tier)")
