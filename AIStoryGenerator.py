import streamlit as st
import requests
import json
from datetime import datetime

# Configuration
MODEL_NAME = "mistralai/Mistral-7B-v0.1"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

def generate_story(prompt, hf_token):
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": f"""Write a 250-word story about: {prompt}
        Requirements:
        - 3 paragraphs
        - Vivid descriptions
        - Twist ending""",
        "parameters": {
            "max_new_tokens": 350,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        # Handle all possible API responses
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list):
                return result[0]['generated_text']
            elif isinstance(result, dict) and 'generated_text' in result:
                return result['generated_text']
            else:
                return f"Unexpected response format: {result}"
                
        elif response.status_code == 503:
            # Model loading case
            try:
                wait_time = int(response.json().get('estimated_time', 30))
                return f"Model is loading... Please wait {wait_time} seconds and try again"
            except:
                return "Model is loading... Please try again later"
                
        else:
            return f"API Error {response.status_code}: {response.text}"
            
    except requests.exceptions.RequestException as e:
        return f"Connection failed: {str(e)}"
    except json.JSONDecodeError:
        return "Invalid API response format"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Mistral-7B Story Generator")
st.title("📖 AI Story Generator")

# Token input (safer than secrets for debugging)
hf_token = st.text_input(
    "Hugging Face Token",
    type="password",
    help="Get one at https://huggingface.co/settings/tokens"
)

prompt = st.text_area(
    "Your story prompt:", 
    "A mysterious door appears in the forest",
    height=100
)

if st.button("✨ Generate Story") and hf_token:
    with st.spinner("Creating your story..."):
        story = generate_story(prompt, hf_token)
        
        if story.startswith(("API Error", "Connection failed", "Unexpected")):
            st.error(story)
        elif story.startswith("Model is loading"):
            st.warning(story)
        else:
            st.subheader("Your Story")
            st.write(story)
            st.download_button(
                "📥 Download Story",
                story,
                file_name=f"story_{datetime.now().strftime('%Y%m%d')}.txt"
            )

# Debug info
st.markdown("---")
st.caption(f"Model: {MODEL_NAME} | Last update: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
