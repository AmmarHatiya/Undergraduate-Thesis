# Get a csv format list of all the image names in dataset
import os
import csv

# Path to the folder containing the images
folder_path = "../images/"

# List all filenames in the folder
file_names = os.listdir(folder_path)

# Path to the CSV file
csv_file_path = "file_names.csv"

# Write the filenames to a CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["File Names"])  # Write header
    for file_name in file_names:
        writer.writerow([file_name])
