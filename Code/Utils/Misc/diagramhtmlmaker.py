import os
import xml.etree.ElementTree as ET
import csv

# Folder containing SVG images
image_folder = "images"

# CSV file containing image information
csv_file = "diagram_Images.csv"

# Create HTML file
html_filename = "diagram_Images_display.html"

# Open CSV file to read image information
images_to_display = []
with open(csv_file, "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header
    for row in reader:
        image_name = row[1]
        image_path = row[2]
        images_to_display.append((image_name, image_path))

# Open HTML file for writing
with open(html_filename, "w") as html_file:
    # Write HTML header
    html_file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Image Dataset</title>\n</head>\n<body>\n")

    # Iterate through images to display
    for image_name, image_path in images_to_display:
        # Check if image exists
        if os.path.exists(image_path):
            # Read SVG content from file
            # Update the part where SVG content is read from the file
            with open(os.path.join(image_folder, image_name+".svg"), "r") as svg_file:
                svg_content = svg_file.read()


            # Parse SVG content to extract dimensions
            svg_tree = ET.ElementTree(ET.fromstring(svg_content))
            svg_root = svg_tree.getroot()

            # Extract viewBox dimensions from the SVG root element
            viewBox = svg_root.get("viewBox")
            if viewBox:
                viewBox_dimensions = viewBox.split()
                min_x, min_y, width, height = map(float, viewBox_dimensions)
            else:
                # Set default dimensions if viewBox is not found
                min_x, min_y, width, height = 0, 0, 200, 200

            # Write HTML code to display the SVG image and filename
            html_file.write(f'<div style="display: inline-block; margin: 10px;">\n')
            html_file.write(f'<svg viewBox="{min_x} {min_y} {width} {height}" width="200" height="200">{svg_content}</svg>\n')
            html_file.write(f'<p style="text-align: center;">({image_name})</p>\n')
            html_file.write(f'</div>\n')
        else:
            print(f"Image {image_name} not found.")

    # Write HTML footer
    html_file.write("</body>\n</html>")

print(f"HTML file '{html_filename}' has been created successfully.")

