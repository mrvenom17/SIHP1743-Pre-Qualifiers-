from PIL import Image
import pytesseract
import openai
import glob
from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv("API.env")
if dotenv_path == "":
    print("No .env file found")
else:
    load_dotenv(dotenv_path)

# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')


# Initialize OpenAI API key
openai.api_key = 'your_openai_api_key'

def extract_text_from_image(image_path):
    """Use OCR to extract text from the image."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def chatgpt_analyze_text(extracted_text):
    """Analyze the text extracted from the image using ChatGPT."""
    prompt = f"Analyze the following text and provide insights: {extracted_text}"

    # Generate a response from ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or 'gpt-4' if available
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()

# Specify the folder containing the images
image_folder = "screenshots" 

# Get a list of all image files in the folder
image_files = glob.glob(f"{image_folder}/*.png") + glob.glob(f"{image_folder}/*.jpg")  # Add more extensions if needed

# Step 1: Extract text from the image using OCR
extracted_text = extract_text_from_image(image_files)

# Step 2: Analyze extracted text using ChatGPT
analysis = chatgpt_analyze_text(extracted_text)

# Step 3: Print the analysis
print(analysis)
