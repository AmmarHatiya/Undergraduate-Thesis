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
csv_file = "basePrompt.csv"

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
                        Generate 5 questions and answers about this image, which can be answered by the image.
                        Format it as a dictionary where keys are questions, and answers are values.
                        For example: {"Q1":"A1", "Q2":"A2", "Q3":"A3", "Q4":"A4", "Q5":"A5"}
                        Aside from that, The response shouldn't be json and no other text/values should be present in the response.
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
                    # print("Image ", image_id, " ("+ image_name+") Q&A written to CSV")
            image_id += 1
        except Exception as e:
            print(f"E: Error processing image {image_name}: {e}, Response:", response.json()['choices'][0]['message']['content'])
        
print("Responses written to CSV file.")