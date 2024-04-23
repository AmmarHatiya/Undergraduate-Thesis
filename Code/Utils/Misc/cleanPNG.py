# Deletes all png images from the images/ folder

import os

# Define the folder containing images
image_folder = "../images"

# Iterate through files in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(".png"):
        file_path = os.path.join(image_folder, filename)
        os.remove(file_path)
        print(f"Deleted file: {file_path}")

print("PNG files deleted.")