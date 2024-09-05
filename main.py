import openai
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
from image import chatgpt_analyze_text  # Ensure the `image` module contains this function

# Load the .env file to get the API key
dotenv_path = find_dotenv("API.env")
if dotenv_path == "":
    print("No .env file found")
else:
    load_dotenv(dotenv_path)

# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Ensure OpenAI API key is set before proceeding
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Ensure it's set in your API.env file.")

openai.api_key = openai_api_key  # Set the API key for OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)
# Function to analyze image descriptions
def analyze_descriptions(image_descriptions):
    for description in image_descriptions:
        response = chatgpt_analyze_text(description)  # Call the function from the `image.py` file
        print(f"Description: {description}\nAnalysis: {response}\n")

# Sample usage (can be removed in Flask integration):
if __name__ == "__main__":
    sample_image_descriptions = [
        "A scenic view of mountains with a river flowing through.",
        "A busy city street with cars, pedestrians, and tall buildings."
    ]
    analyze_descriptions(sample_image_descriptions)
