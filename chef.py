import openai
import streamlit as st

# Set your OpenAI API key (use your own API key here)
openai.api_key = st.secrets["openai_api_key"]

# Define the project and location (used for your setup)
PROJECT_ID = st.secrets["PROJECT_ID"]
LOCATION = st.secrets["LOCATION"]

# Define the model you want to use
model_name = "gpt-4"  # You can choose any other model like "gpt-3.5-turbo"

def get_gemini_flash_text_response(prompt: str):
    """
    Function to get the response from the OpenAI GPT model using chat completion API.
    """
    try:
        # Prepare the conversation messages
        messages = [
            {"role": "system", "content": "You are a helpful chef."},  # System message for behavior
            {"role": "user", "content": prompt}  # User prompt
        ]
        
        # Call the OpenAI API with the new chat completion method
        response = openai.chat.Completion.create(
            model=model_name,  # Specify the model
            messages=messages   # Send the messages as input
        )
        
        # Extract the content from the response
        result = response['choices'][0]['message']['content']
        return result
    
    except Exception as e:
        # Handle any errors that occur during the request
        st.error(f"Error: {e}")
        return None

# Streamlit interface
st.title("Chef Assistant")

# User input for the recipe or query
prompt = st.text_input("What do you want to cook today?")

if prompt:
    # Get the result from the model
    result = get_gemini_flash_text_response(prompt)
    
    if result:
        # Display the result to the user
        st.write("Here's your recipe:")
        st.write(result)
