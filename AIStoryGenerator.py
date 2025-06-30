import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

@st.cache_resource
def load_model():
    model_name = "mistralai/Mistral-7B-v0.1"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        load_in_4bit=True
    )
    
    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=400,
        temperature=0.7,
        top_p=0.95,
        do_sample=True,
        early_stopping=True,
        pad_token_id=tokenizer.eos_token_id
    )

def main():
    st.title("✨ AI Story Generator (Mistral-7B)")
    st.caption("Example Format of Story Prompt: Write a complete short story about a girl who wants to be a singer under 250 words")
    
    prompt = st.text_area(
        "Enter your story prompt:", 
        value="",
        height=100,
        placeholder="Type your story prompt here..."
    )
    
    if st.button("Generate Story"):
        if not prompt.strip():
            st.warning("Please enter a story prompt!")
        else:
            generator = load_model()
            with st.spinner("🧙‍♂️ Crafting your story..."):
                formatted_prompt = f"""Write a complete short story under 250 words based on:
                PROMPT: {prompt}
                REQUIREMENTS:
                - Proper beginning, middle, and end
                - At least 3 paragraphs
                - Complete resolution
                STORY:"""
                
                result = generator(formatted_prompt)
                full_story = result[0]['generated_text'].split("STORY:")[-1].strip()
                
                if len(full_story.split()) < 50:
                    st.error("Story too short - please try again!")
                else:
                    st.subheader("Your Complete Story")
                    st.write(full_story)
                    
                    st.download_button(
                        "📥 Download Story",
                        full_story,
                        file_name="complete_story.txt"
                    )

if __name__ == "__main__":
    main()
