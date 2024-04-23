# Splits csv file containing all images in nissan images dataset into 3 distinct ones depending on image label type
import csv

# Function to read CSV file
def read_csv(filename):
    data = []
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            data.append(row)
    return data

# Function to write CSV file
def write_csv(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["image_id", "image_name", "image_path", "label"])
        writer.writerows(data)

# Read binaryLabeling.csv file
labels_data = read_csv('DiagramLabelsGT.csv')

# Separate data based on labels
other_data = []
itemdictionary_data = []
procedural_data = []

for label_row in labels_data:
    image_id = int(label_row[0])
    image_name = label_row[1]
    image_path = label_row[2]
    label = label_row[3]
    
    if label == "Diagram-Other":
        other_data.append([image_id, image_name, image_path, label])
    elif label == "Diagram-ItemDictionary":
        itemdictionary_data.append([image_id, image_name, image_path, label])
    elif label == "Diagram-Procedural":
        procedural_data.append([image_id, image_name, image_path, label])

# Write data to separate CSV files
write_csv('other_diagram_Images.csv', other_data)
write_csv('procedural_diagram_Images.csv', procedural_data)
write_csv('itemdictionary_diagram_Images.csv', itemdictionary_data)

print("Files separated successfully.")
