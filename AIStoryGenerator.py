import streamlit as st
import google.generativeai as genai
import os

# --- 1. Configure Google Gemini API ---
# It's crucial to handle your API key securely.
# For Streamlit Cloud deployment, use st.secrets.
# For local testing, you can set it as an environment variable (recommended)
# or temporarily hardcode it (NOT recommended for production or sharing).

# Try to get API key from Streamlit secrets first (for deployment)
# If not found, try from environment variables (for local development)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    API_KEY = os.getenv("GEMINI_API_KEY")

# If API key is still not found, display an error and stop the app
if not API_KEY:
    st.error(
        "Gemini API Key not found! Please set the 'GEMINI_API_KEY' "
        "in your Streamlit secrets (for deployment) or as an "
        "environment variable (for local testing)."
    )
    st.info(
        "You can get your API key from Google AI Studio: "
        "https://aistudio.google.com/app/apikey"
    )
    st.stop() # Stop the app if no API key is found

# Configure the generative AI model with your API key
genai.configure(api_key=API_KEY)

# Initialize the Generative Model
# 'gemini-pro' is recommended for text generation tasks and is generally
# available on the free tier.

model = genai.GenerativeModel('gemini-2.0-flash')
# --- 2. Streamlit App User Interface (UI) ---

# Set basic page configuration for the Streamlit app
st.set_page_config(
    page_title="AI Story Generator",
    page_icon="✍️",
    layout="centered", # 'centered' or 'wide'
    initial_sidebar_state="collapsed" # 'auto', 'expanded', or 'collapsed'
)

# Custom CSS for a more appealing look
st.markdown(
    """
    <style>
    /* Main container styling */
    .main {
        background-color: #f0f2f6; /* Light gray background */
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        font-family: 'Inter', sans-serif; /* Use Inter font */
    }

    /* Header styling */
    h1 {
        color: #2c3e50; /* Dark blue-gray */
        text-align: center;
        margin-bottom: 30px;
        font-size: 2.5em;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }

    /* Button styling */
    .stButton>button {
        background-color: #4CAF50; /* Green */
        color: white;
        border-radius: 12px; /* More rounded corners */
        border: none;
        padding: 12px 28px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease; /* Smooth transition for hover effects */
        box-shadow: 0 5px 15px 0 rgba(0,0,0,0.2); /* Subtle shadow */
        display: block; /* Make button take full width of its container */
        margin: 20px auto; /* Center the button */
    }
    .stButton>button:hover {
        background-color: #45a049; /* Darker green on hover */
        box-shadow: 0 8px 20px 0 rgba(0,0,0,0.25); /* Larger shadow on hover */
        transform: translateY(-3px); /* Slight lift effect */
    }
    .stButton>button:active {
        transform: translateY(0); /* Press effect */
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Text input and text area styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #dcdcdc; /* Light gray border */
        padding: 12px;
        box-shadow: inset 0 1px 5px rgba(0,0,0,0.08); /* Inner shadow */
        font-size: 1em;
        color: #333;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #4CAF50; /* Green border on focus */
        box-shadow: 0 0 0 0.2rem rgba(76, 175, 80, 0.25); /* Light green glow on focus */
        outline: none; /* Remove default outline */
    }

    /* Story output display area */
    .story-output {
        background-color: #ffffff; /* White background for story */
        border-left: 6px solid #2196F3; /* Blue left border for emphasis */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-top: 30px;
        white-space: pre-wrap; /* Preserves whitespace and line breaks from model output */
        font-size: 1.1em;
        line-height: 1.7;
        color: #333;
    }

    /* Info/Warning messages */
    .stAlert {
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True # Required to inject custom CSS
)

# Application Title
st.title("✍️ AI Story Generator")

# Introduction text
st.write(
    "Enter a prompt below : "
    
)

# Input field for the user's story prompt
prompt = st.text_input(
    "What kind of story do you want to generate?",
    placeholder="e.g., A futuristic detective solving a case in a neon-lit city, "
                "a talking animal embarking on a magical adventure, "
                "a historical mystery set in ancient Rome..."
)

# Button to trigger story generation
if st.button("Generate Story"):
    if prompt: # Check if the prompt is not empty
        with st.spinner("Crafting your masterpiece... Please wait."):
            try:
                # Call the Gemini Pro model to generate content
                # The prompt is sent directly to the model.
                response = model.generate_content(prompt)

                # Display the generated story
                # Using markdown with custom class for styling
                st.markdown(f"<div class='story-output'>{response.text}</div>", unsafe_allow_html=True)

            except Exception as e:
                # Catch any errors during API call or response processing
                st.error(f"Oops! An error occurred while generating the story: {e}")
                st.warning(
                    "Please check your internet connection and ensure your "
                    "Gemini API key is valid and correctly configured."
                )
    else:
        # Warn the user if the prompt field is empty
        st.warning("Please enter a prompt to ignite the story!")

# Footer for the application
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Google Gemini API.")
