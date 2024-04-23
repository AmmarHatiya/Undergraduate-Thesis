# 
# Image to Description: From an image, generate an exhaustive description about the image. 
# 

import base64
import requests
import cairosvg
import PIL.Image
from io import BytesIO
import os
import csv
import ast

# OpenAI API Key
api_key = "-----PASTE-API-KEY-HERE-----"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Define the folder containing images
image_folder = "images"
# Define the CSV file name
csv_file = "descriptions.csv"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
# Function to save SVG as PNG with white background
def save_svg_as_png_with_white_background(svg_path, output_path):
    # Read SVG content from file
    with open(svg_path, 'r') as svg_file:
        svg_content = svg_file.read()

    # Convert SVG to PNG using cairosvg with a white background
    cairosvg.svg2png(
        bytestring=svg_content.encode('utf-8'),
        write_to=output_path,
        background_color='white'
    )

# Function to prompt for response
def prompt(target_image):
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": """
                        Provide a comprehensive description of the attached image.
                        Nothing else should be in your response.
                        Start the response with "Response:" if successful, and with "E:" otherwise.
                        For example: Response: ....
                        """
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{target_image}"
                }
              }
            ]
          }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response

# Initialize image ID
image_id = 1

# Open CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['image_id', 'image_name', 'description'])

    # Iterate through image files in the folder
    for filename in os.listdir(image_folder):
        if filename.endswith(".svg"):
            image_name = os.path.splitext(filename)[0]
            image_path = os.path.join(image_folder, filename)
            save_svg_as_png_with_white_background(image_path, image_path[:-3] + "png")
            image_path = image_path[:-3] + "png"
            base64_image = encode_image(image_path)

            response = prompt(base64_image)

            if 'error' in response.json():
                print(f"E: {response.json()['error']}")
            else:
                response_text = response.json()['choices'][0]['message']['content'].strip()
                if response_text.startswith("Response:"):
                    description = response_text.replace("Response:", "").strip().replace("\n", " ")
                    writer.writerow([image_id, image_name, f'"{description}"'])
                    image_id += 1
                else:
                    print(f"E: Unexpected response format for image {image_id}:", response_text)
        

print("Descriptions written to CSV file.")
