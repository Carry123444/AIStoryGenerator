import streamlit as st
import requests

# 1. Get your token from: https://huggingface.co/settings/tokens
# 2. Accept model terms: https://huggingface.co/mistralai/Mistral-7B-v0.1
HF_TOKEN = st.secrets.get("HF_API_TOKEN") or "your_token_here"
MODEL_NAME = "mistralai/Mistral-7B-v0.1"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

def generate_story(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Verified working prompt format
    payload = {
        "inputs": f"""<s>[INST] Write a story about: {prompt}
        - 3 paragraphs
        - Vivid descriptions
        - Twist ending [/INST]""",
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json()[0]['generated_text'].split("[/INST]")[-1].strip()
        elif response.status_code == 404:
            st.error("""
            Model not found. Ensure:
            1. You've accepted the model terms at:
               https://huggingface.co/mistralai/Mistral-7B-v0.1
            2. Your token has 'read' access
            """)
        else:
            return f"API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Connection failed: {str(e)}"

# Streamlit UI
st.title("📖 Mistral-7B Story Generator")
prompt = st.text_area("Prompt:", "A girl who wants to be a singer")

if st.button("Generate"):
    with st.spinner("Generating..."):
        story = generate_story(prompt)
        if story and not story.startswith("API Error"):
            st.write(story)
            st.download_button("Download", story)
