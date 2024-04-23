# Initial Image Dataset, Label as either Diagram or Icon
import base64
import requests
import cairosvg
import PIL.Image
from io import BytesIO
import os
import csv

# OpenAI API Key
api_key = "-----PASTE-API-KEY-HERE-----"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Define the folder containing images
image_folder = "images"

# Define the CSV file name
csv_file = "binaryLabeling.csv"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to write response to CSV
def write_to_csv(image_id, file_name, image_path, response):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([image_id, file_name, image_path, response])

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
                Label the following image as 1 of the following categories: 
                Icon: If the picture only contains an icon/symbol and nothing else, 
                Diagram (everything else)
                Your response should only contain the category, nothing else and no Punctuation.
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

# Initialize id counter
id_counter = 1

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
            error = response.json()['error']
            print("Failed to label ", image_name)
        else:
            response_text = response.json()['choices'][0]['message']['content']
            print(f"Response for {image_name}: {response_text}")
            write_to_csv(id_counter, image_name, image_path, response_text)
            id_counter += 1

print("All responses saved to CSV.")
