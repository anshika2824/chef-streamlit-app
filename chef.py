import openai
import streamlit as st
import logging

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Ensure your API key is in your secrets

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- STREAMLIT UI ---
st.header("👨‍🍳 AI Chef Powered by GPT-3")

st.write("Using GPT-3 to generate custom meal plans!")

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

# --- GENERATE BUTTON ---
if st.button("🍽️ Generate My Recipes"):
    with st.spinner("Cooking up something delicious..."):
        try:
            # Make API call to OpenAI GPT-3
            response = openai.Completion.create(
                engine="text-davinci-003",  # Use the Davinci model (GPT-3)
                prompt=prompt,
                temperature=0.7,
                max_tokens=1500,
            )

            # Display the result
            result = response.choices[0].text.strip()
            st.subheader("Here’s your custom meal plan:")
            st.write(result)
            logging.info(result)
        except Exception as e:
            st.error("Oops! Something went wrong.")
            st.exception(e)
