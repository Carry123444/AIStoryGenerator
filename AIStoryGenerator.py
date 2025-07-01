import streamlit as st
import requests

# No API token required for public models
MODEL_NAME = "gpt2"  # Switch to any public model
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

def generate_story(prompt):
    payload = {
        "inputs": f"Write a short story about {prompt} with a twist ending:",
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.9
        }
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        return f"Error: {response.text}"
    except Exception as e:
        return f"Connection failed: {str(e)}"

# Streamlit UI
st.title("📖 Free Story Generator")
prompt = st.text_input("Enter your prompt:", "A cat who solves mysteries")

if st.button("Generate"):
    st.write(generate_story(prompt))
