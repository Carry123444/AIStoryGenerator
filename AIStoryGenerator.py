import streamlit as st
import requests

# This will work with the new token format
def generate_story(prompt):
    headers = {"Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"}
    payload = {
        "inputs": f"Write a story about {prompt}",
        "parameters": {"max_new_tokens": 300}
    }
    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1",
        headers=headers,
        json=payload
    )
    return response.json()[0]['generated_text']

st.title("Story Generator")
prompt = st.text_input("Enter prompt")
if st.button("Generate"):
    st.write(generate_story(prompt))
