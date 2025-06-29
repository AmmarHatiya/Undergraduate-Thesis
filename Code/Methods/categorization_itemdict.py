# 
# 1-Shot + Categorization (Item Dictionary) Prompt Engineering Method
# 

import base64
import requests
import cairosvg
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
csv_file = "category_itemdict_w_example.csv"

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

# Process Example Inputs
image_path = "./images/WBA0012X=WBA0012X=1=en, ja=High.svg"[:-3] + "png"
save_svg_as_png_with_white_background(image_path[:-3]+"svg", image_path)
example_image = encode_image(image_path)

example_qa = """
{"Where is the side ventilator located in my vehicle?":"The side ventilator is located at the end of the dashboard on the driver and passenger sides, near the doors.",
"Where can I find the meters and gauges in my vehicle?":"The meters and gauges are positioned directly in front of the steering wheel in the driver's line of sight for easy monitoring",
"Where is the Head-Up Display (HUD) located?":"The Head-Up Display (HUD), if your vehicle is equipped with it, projects important information onto the windshield directly in the driver’s view.",
"Where is the push-button power switch located?":"The push-button power switch, used to start and stop the engine, is located on the dashboard or the center console, depending on the vehicle model.",
"Where is the hood release handle found in my vehicle?":"The hood release handle is typically positioned inside the vehicle, on the lower left side of the dashboard or near the kick panel."}
"""

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
                "text": """Generate 5 questions and answers about the attached image, which can be answered by the image.
                The given image is an Item dictionary image, meaning that it numerically labels different parts present in the image.
                
                Format the questions and answers as a dictionary where keys are questions, and answers are values.
               For example: {"Q1":"A1", "Q2":"A2", "Q3":"A3", "Q4":"A4", "Q5":"A5"}
               Aside from that, The response shouldn't be json and no other text/values should be present in the response. Here is the image:
"""
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{target_image}"
                }
              },
              {
                "type": "text",
                "text": "Here is an example for you to follow (Image with questions and answers): " + example_qa
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{example_image}"
                }
              }
            ]
          }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response


# Load image names from itemdict_diagram_Images.csv
image_names = set()
with open("itemdictionary_diagram_Images.csv", mode='r', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for row in reader:
        image_names.add(row[1])

# Initialize image ID
image_id = 1

# Iterate through image files in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(".svg"):
        image_name = os.path.splitext(filename)[0]
        if image_name not in image_names:
            continue

        image_path = os.path.join(image_folder, filename)
        save_svg_as_png_with_white_background(image_path, image_path[:-3] + "png")
        image_path = image_path[:-3] + "png"
        base64_image = encode_image(image_path)

        response = prompt(base64_image)
        
        if 'error' in response.json():
            print(f"E: Error processing image {image_name}: ", response.json()['error']['message'])
            continue  # Skip processing further if an error occurs
            
        try:
            response_dict_str = response.json()['choices'][0]['message']['content']
            response_dict = ast.literal_eval(response_dict_str)

            # Open CSV file for writing
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)

                # Write each question-answer pair to CSV
                for qa_id, (question, answer) in enumerate(response_dict.items(), start=1):
                    # Format fields with quotation marks where necessary
                    formatted_question = f'"{question}"'
                    formatted_answer = f'"{answer}"'
                    writer.writerow([image_id, image_name, qa_id, formatted_question, formatted_answer])
                    # Print a success message
                    print(f"SUCCESS: Processing image {image_name}")

            # Increment image ID
            image_id += 1
        except Exception as e:
            # Print an error message if an exception occurs during processing
            print(f"E: Error processing image {image_name}: {e}, Response:", response.json()['choices'][0]['message']['content'])

# Print a final message
print("Responses written to CSV file.")