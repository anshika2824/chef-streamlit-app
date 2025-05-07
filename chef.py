import os
import json
import streamlit as st
import logging

# Configure console logging
logging.basicConfig(level=logging.INFO)

# --- AUTH SETUP WITH GCP SECRETS ---
# Write service account JSON key to a temp file
creds = st.secrets["GCP_SERVICE_ACCOUNT"]
key_path = "/tmp/gcp_key.json"
with open(key_path, "w") as f:
    f.write(creds)

# Set environment variable for Google SDKs
import os
from google.cloud import vertexai

# Set up environment variable (you can also rely on it being set outside the script)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/anshikarana/Downloads/chef-streamlet-deaaa1ac020a.json"


# Read project ID and region
PROJECT_ID = st.secrets["PROJECT_ID"]
LOCATION = st.secrets.get("LOCATION", "us-central1")

# --- IMPORT VERTEX AI ---
import vertexai
from vertexai import init
from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory
)

# Initialize Vertex AI
init(project=PROJECT_ID, location=LOCATION)

# --- MODEL LOADING ---
@st.cache_resource
def load_models():
    return GenerativeModel("gemini-2.0-flash-001")

text_model_flash = load_models()

# --- FUNCTION TO GET RESPONSE ---
def get_gemini_flash_text_response(
    model: GenerativeModel,
    contents: str,
    generation_config: GenerationConfig,
    stream: bool = True,
):
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    responses = model.generate_content(
        contents,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=stream,
    )

    result = []
    for r in responses:
        result.append(getattr(r, "text", ""))
    return " ".join(result)

# --- STREAMLIT UI ---
st.header("👨‍🍳 AI Chef Powered by Gemini Flash", divider="gray")

st.write("Using Gemini Flash - Text-only model")

st.subheader("Tell us your preferences:")

cuisine = st.selectbox(
    "What cuisine do you desire?",
    ("American", "Chinese", "French", "Indian", "Italian", "Japanese", "Mexican", "Turkish"),
    index=None,
    placeholder="Select your desired cuisine."
)

dietary_preference = st.selectbox(
    "Do you have any dietary preferences?",
    ("Diabetes", "Gluten free", "Halal", "Keto", "Kosher", "Lactose Intolerance", "Paleo", "Vegan", "Vegetarian", "None"),
    index=None,
    placeholder="Select your dietary preference."
)

allergy = st.text_input("Enter any food allergy:", value="peanuts")
ingredient_1 = st.text_input("Enter your first ingredient:", value="ahi tuna")
ingredient_2 = st.text_input("Enter your second ingredient:", value="chicken breast")
ingredient_3 = st.text_input("Enter your third ingredient:", value="tofu")
wine = st.radio("Select wine preference:", ["Red", "White", "None"])

# --- PROMPT GENERATION ---
prompt = f"""
I am a Chef. I need to create {cuisine} recipes for customers who want {dietary_preference} meals.
Do not include any ingredients that may trigger their {allergy} allergy.
I have {ingredient_1}, {ingredient_2}, and {ingredient_3} in my kitchen along with other ingredients.
The customer's wine preference is {wine}.
Please provide meal recommendations.

For each recommendation include:
- A title
- Preparation instructions
- Time to prepare
- Wine pairing
- Calories and nutritional facts
"""

# --- GENERATION CONFIG ---
config = GenerationConfig(temperature=0.8, max_output_tokens=2048)

# --- GENERATE BUTTON ---
if st.button("🍽️ Generate My Recipes"):
    with st.spinner("Cooking up something delicious..."):
        try:
            result = get_gemini_flash_text_response(text_model_flash, prompt, config)
            st.subheader("Here’s your custom meal plan:")
            st.write(result)
            logging.info(result)
        except Exception as e:
            st.error("Oops! Something went wrong.")
            st.exception(e)
