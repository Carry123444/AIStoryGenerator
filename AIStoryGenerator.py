import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1"
API_TOKEN = "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"

def query(payload):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def main():
    st.title("✨ AI Story Generator (Mistral-7B)")
    
    prompt = st.text_area(
        "Enter your story prompt:", 
        placeholder="e.g., A girl who wants to be a singer"
    )
    
    if st.button("Generate Story"):
        if not prompt.strip():
            st.warning("Please enter a prompt!")
        else:
            with st.spinner("Generating..."):
                formatted_prompt = f"Write a complete 250-word story about: {prompt}"
                output = query({
                    "inputs": formatted_prompt,
                    "parameters": {
                        "max_new_tokens": 300,
                        "temperature": 0.7
                    }
                })
                
                if isinstance(output, list) and len(output) > 0:
                    st.write(output[0]['generated_text'])
                else:
                    st.error("Failed to generate story. Try again later.")

if __name__ == "__main__":
    main()
