# import csv

# # Open the input and output CSV files
# with open('GT_Item-Dict.csv', mode='r', encoding='utf-8-sig') as csv_input_file:
#     with open('GT_ItemDict.csv', mode='w', encoding='utf-8', newline='') as csv_output_file:
#         csv_reader = csv.DictReader(csv_input_file)
#         fieldnames = ['Image ID', 'QA ID', 'Question', 'Answer']
#         csv_writer = csv.DictWriter(csv_output_file, fieldnames=fieldnames)
#         csv_writer.writeheader()
        
#         current_image_id = None
#         next_line_answer = False  # Flag to indicate if the next line contains an answer
#         qa_id = 1  # Initialize the question ID
        
#         for row in csv_reader:
#             image_id = row['Image ID'].strip()
#             qas = row['GT QAs'].split('\n')
            
#             # If it's a new image, reset the question ID counter
#             if image_id != current_image_id:
#                 current_image_id = image_id
#                 qa_id = 1
            
#             # Process each question-answer pair
#             for qa_pair in qas:
#                 if '**Q**' in qa_pair:
#                     question = qa_pair.replace('**Q**: ', '').strip()[3:]
#                     next_line_answer = True
#                 elif '**A**' in qa_pair:
#                     answer = qa_pair.replace('**A**: ', '').strip()
#                     # Wrap question and answer with triple quotes
#                     question = '"""' + question + '"""'
#                     answer = '"""' + answer + '"""'
#                     # Write to the output CSV file
#                     csv_writer.writerow({'Image ID': image_id, 'QA ID': qa_id, 'Question': question, 'Answer': answer})
#                     qa_id += 1  # Increment the question ID for the next question
#                     next_line_answer = False
#                 elif next_line_answer:
#                     answer = qa_pair.strip()
#                     # Wrap answer with triple quotes
#                     answer = '"""' + answer + '"""'
#                     # Write to the output CSV file
#                     csv_writer.writerow({'Image ID': image_id, 'QA ID': qa_id, 'Question': question, 'Answer': answer})
#                     qa_id += 1  # Increment the question ID for the next question
#                     next_line_answer = False


# import csv
# import re

# # Open the input and output CSV files
# with open('GT_Procedural.csv', mode='r', encoding='utf-8-sig') as csv_input_file:
#     with open('output.csv', mode='w', encoding='utf-8', newline='') as csv_output_file:
#         csv_writer = csv.writer(csv_output_file)
#         csv_writer.writerow(['id', 'image_name', 'qa_id', 'question', 'answer'])  # Write header
        
#         image_id_map = {}  # To store image IDs
#         qa_id_map = {}  # To store QA IDs
        
#         for row in csv.reader(csv_input_file):
#             image_name = row[0]
#             questions_answers = row[1].split('\n')
            
#             # Check if the image name already has an ID assigned
#             if image_name not in image_id_map:
#                 image_id_map[image_name] = len(image_id_map) + 1
#                 qa_id_map[image_name] = 1
            
#             image_id = image_id_map[image_name]
#             qa_id = qa_id_map[image_name]
            
#             question = ''
#             answer = ''
#             for qa in questions_answers:
#                 qa = qa.strip()
#                 if qa.startswith('Q'):
#                     if question:  # If there's a question already, write the previous pair
#                         csv_writer.writerow([image_id, image_name, qa_id, f'"""{question}"""', f'"""{answer.strip()}"""'])
#                         qa_id += 1
#                     question = qa[3:]
#                     answer = ''
#                 elif qa.startswith('A'):
#                     answer += qa[3:] + '\n'
            
#             # Write the last question-answer pair
#             csv_writer.writerow([image_id, image_name, qa_id, f'"""{question}"""', f'"""{answer.strip()}"""'])

import pandas as pd

# Read the CSV file
df = pd.read_csv('GT_ItemDict.csv')

# Initialize a dictionary to store the mapping of image_name to id
image_name_to_id = {}

# Initialize the id counter
id_counter = 1

# Iterate through the DataFrame
for index, row in df.iterrows():
    image_name = row['image_name']
    # If the image_name is not in the dictionary, assign it a new id
    if image_name not in image_name_to_id:
        image_name_to_id[image_name] = id_counter
        id_counter += 1
    # Assign the id to the row
    df.at[index, 'id'] = image_name_to_id[image_name]

# Convert the 'id' column to integer
df['id'] = df['id'].astype(int)

# Reorder the columns with 'id' as the first column
df = df[['id', 'image_name', 'qa_id', 'question', 'answer']]

# Save the DataFrame back to a CSV file
df.to_csv('modified_file.csv', index=False)


