import streamlit as st
import requests

# Configure through Streamlit secrets
HF_TOKEN = st.secrets["HF_API_TOKEN"]
MODEL_NAME = "mistralai/Mistral-7B-v0.1"  # Base model
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

def generate_story(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Special prompt formatting for base Mistral
    formatted_prompt = f"""Write a detailed 250-word story about: {prompt}
    Structure:
    1. Engaging introduction
    2. Character development
    3. Surprising conclusion
    
    Story:"""
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 350,
            "temperature": 0.8,
            "top_p": 0.9,
            "do_sample": True
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()[0]['generated_text'].split("Story:")[-1].strip()
        elif response.status_code == 503:
            est_time = response.json().get('estimated_time', 30)
            st.warning(f"Model is loading... Please wait {int(est_time)} seconds")
        else:
            st.error(f"API Error: {response.text}")
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")
    return None

# Streamlit UI
st.set_page_config(page_title="Mistral-7B Story Generator")
st.title("AI Story Generator (Mistral-7B)")

with st.sidebar:
    st.markdown("""
    **How to get started**:
    1. Get a [free Hugging Face token](https://huggingface.co/settings/tokens)
    2. Add it to your Streamlit secrets
    3. Enter your prompt below
    """)

prompt = st.text_area(
    "What's your story about?",
    "A mysterious door appears in the forest",
    height=100
)

if st.button("✨ Generate Story"):
    if not prompt.strip():
        st.warning("Please enter a prompt")
    else:
        with st.spinner("Generating your story..."):
            story = generate_story(prompt)
            if story:
                st.subheader("Your Generated Story")
                st.write(story)
                st.download_button(
                    "📥 Download Story",
                    story,
                    file_name="story.txt"
                )

# Footer
st.markdown("---")
st.caption(f"Using {MODEL_NAME} via Hugging Face API")
