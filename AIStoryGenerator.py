import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# Configure API - Add your key in Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generate_story(prompt):
    try:
        # Using the exact 'gemini-pro' model name
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(
            f"""Write a compelling 250-word short story based on:
            **Prompt**: {prompt}
            
            **Requirements**:
            - 3 clear paragraphs (beginning, middle, end)
            - Include sensory details (sights, sounds)
            - Unexpected but satisfying ending
            
            **Story**:""",
            generation_config={
                "max_output_tokens": 500,
                "temperature": 0.8,
                "top_p": 0.9
            },
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE"
            }
        )
        return response.text
        
    except exceptions.NotFound as e:
        st.error("Model error: Ensure you're using 'gemini-pro' as the model name")
        return ""
    except exceptions.InvalidArgument as e:
        st.error("API key error: Check your Google AI Studio key")
        return ""
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return ""

# Streamlit UI
st.set_page_config(page_title="AI Story Generator", layout="wide")
st.title(" AI Story Generator (Gemini)")

prompt = st.text_area(
    "Enter your story idea:", 
    value="",
    height=100,
    help="Example: A robot who dreams of dancing"
)

if st.button("✨ Generate Story", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a story prompt!")
    else:
        with st.spinner("Creating your story (may take 10-20 seconds)..."):
            story = generate_story(prompt)
            if story:
                st.subheader("Your Story")
                st.write(story)
                st.download_button(
                    "📥 Download Story", 
                    story, 
                    file_name="generated_story.txt"
                )

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini Pro (free tier) | Limit: ~1 request/minute")
