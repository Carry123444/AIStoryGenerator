import streamlit as st
import requests
from datetime import datetime

# Configuration
MODEL_NAME = "mistralai/Mistral-7B-v0.1"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

def check_token_validity(token):
    """Verify if the token is valid"""
    test_url = "https://huggingface.co/api/whoami-v2"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(test_url, headers=headers)
        return response.status_code == 200
    except:
        return False

def generate_story(prompt, hf_token):
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": f"""Write a detailed 250-word story about: {prompt}
        Must include:
        - Vivid descriptions
        - Character development
        - Unexpected ending
        
        Story:""",
        "parameters": {
            "max_new_tokens": 350,
            "temperature": 0.8,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json()[0]['generated_text'].split("Story:")[-1].strip()
        else:
            return f"API Error: {response.text}"
    except Exception as e:
        return f"Connection error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Mistral-7B Story Generator")
st.title("📖 Mistral-7B Story Generator")

# Token input (alternative to secrets)
hf_token = st.text_input(
    "Enter Hugging Face Token",
    type="password",
    help="Get one at https://huggingface.co/settings/tokens"
)

if hf_token:
    if not check_token_validity(hf_token):
        st.error("❌ Invalid or expired token! Get a new one.")
    else:
        st.success("✅ Valid token detected")

prompt = st.text_area(
    "Story prompt:", 
    "A scientist discovers a hidden dimension",
    height=100
)

if st.button("Generate Story") and hf_token:
    with st.spinner("Generating..."):
        story = generate_story(prompt, hf_token)
        
        if story.startswith("API Error"):
            st.error(story)
        elif story.startswith("Connection error"):
            st.warning(story)
        else:
            st.subheader("Your Story")
            st.write(story)
            st.download_button("Download", story)

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
