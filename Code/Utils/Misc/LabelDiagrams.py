# Labeling Images 1.1, and 1.2 (see comments)
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
csv_file = "DiagramLabels2.csv"

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
    
    diagram_image_file = "WBA0025X.svg"
    save_svg_as_png_with_white_background(diagram_image_file, f"./{diagram_image_file[:-3]}png")
    image_path = f"./{diagram_image_file[:-3]}png"
    diagram_image = encode_image(image_path)
    
    procedural_image_file = "WBS0027X.svg"
    save_svg_as_png_with_white_background(procedural_image_file, f"./{procedural_image_file[:-3]}png")
    image_path = f"./{procedural_image_file[:-3]}png"
    procedural_image = encode_image(image_path)
#1.2 Labeling Images 0-shot 
       # Label the following image as 1 of the following 3 categories: 
       # 1. "Diagram-ItemDictionary": If the image outlines parts of an item, always numbered to differentiate the different parts.
       # 2. "Diagram-Procedural": If the image illustrates a step-by-step, numbered, procedure that can be followed.
       # 3. "Diagram-Other": If the image doesn't fall into any of the other categories.
       # Your response should only contain the category, nothing else and no Punctuation.

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": """
                Label the following image as 1 of the following 3 categories: 
                1. "Diagram-ItemDictionary": If the image outlines parts of an item. These images are always numbered to differentiate the different parts.
                Here is an example of a "Diagram-ItemDictionary" image:
                """
                },
                {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{diagram_image}"
                }
               },
                {
                "type": "text",
                "text": """ 2. "Diagram-Procedural": If the image is of a clearly labelled step-by-step, numbered, procedure. The Procedure outlined should always be more than 1 step. 
                                Here is an example of a "Diagram-Procedural" image:
                """
                },
                {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{procedural_image}"
                }
                },
                {
                "type": "text",
                "text": """3. "Diagram-Other": If the image doesn't fall into the any of the other categories (i.e. everything else).
                Do not compel the categorization of the image into the first and second categories.
                Your response should only contain the category, nothing else and no Punctuation. Below is the image that needs to be labelled:
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

# Read LabelingImages.csv file
with open('diagram_Images.csv', 'r') as label_file:
    label_reader = csv.reader(label_file)
    next(label_reader)  # Skip header
    for row in label_reader:
        image_id = int(row[0])
        image_name = row[1]
        image_path = row[2]
        label = row[3]

        # Check if image exists in the images folder
        image_file = os.path.join(image_folder, f"{image_name}.svg")
        if os.path.exists(image_file):
            save_svg_as_png_with_white_background(image_file, f"{image_file[:-3]}png")
            image_path = f"{image_file[:-3]}png"
            base64_image = encode_image(image_path)

            response = prompt(base64_image)
            if 'error' in response.json():
                error = response.json()['error']
                print(f"Failed to label {image_name}: {error}")
            else:
                response_text = response.json()['choices'][0]['message']['content']
                print(f"Response for {image_name}: {response_text}")
                write_to_csv(id_counter, image_name, image_path, response_text)
                id_counter += 1
        else:
            print(f"Image {image_name} not found in images folder.")

print("All responses saved to CSV.")
