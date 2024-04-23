# 
# 1-Shot Prompt Engineering Method
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
csv_file = "prompt_w_example.csv"

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
image_path = "./images/WBS0024X=WBS0024X=1=en, ja=High.svg"[:-3] + "png"
save_svg_as_png_with_white_background(image_path[:-3]+"svg", image_path)
example_image = encode_image(image_path)

example_qa = """
{"How do I start my car?":"To start your car, first make sure your foot is firmly pressing the brake pedal. Then, press the start/stop engine button typically located on the dashboard or near the steering wheel.", 
"What does the 'READY' indicator mean on my dashboard?":"The 'READY' indicator on your dashboard signifies that your car's engine is turned on and ready to drive. For electric or hybrid vehicles, this may not always be accompanied by the sound of an engine starting as these cars can operate silently.",
"Do I need to keep pressing the brake pedal while starting the car?":"Yes, you should keep pressing the brake pedal while starting the car. This is a safety feature to ensure that the vehicle doesn't move unexpectedly when starting.",
"Why won't my car start even when I press the brake and the start button?":"If your car doesn't start, check to ensure that the key fob is inside the vehicle and the battery is not depleted. Also, make sure that the gear is in the 'Park' or 'Neutral' position. If these conditions are met and the car still won't start, consult the vehicle's manual or a professional, as there may be an issue with the vehicle's electrical system or the start button itself.", 
"Question_5":"Answer_5"}
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
                Format it as a dictionary where keys are questions, and answers are values.
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
            print(f"SUCCESS: Processing image {image_name}")
            image_id += 1
        except Exception as e:
            print(f"E: Error processing image {image_name}: {e}, Response:", response.json()['choices'][0]['message']['content'])
        
print("Responses written to CSV file.")