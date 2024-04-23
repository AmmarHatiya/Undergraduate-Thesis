import pandas as pd

# Read the CSV file without header
df = pd.read_csv('description_based_Results.csv', header=None, names=['image_id', 'image_name', 'description', 'sentence_srl', 'sentence', 'question'])

# Add a new column 'qa_id' after the 'question' column
df.insert(df.columns.get_loc('question') + 1, 'qa_id', '')

# Initialize a dictionary to keep track of unique questions for each image_name
question_counts = {}

# Iterate over each row in the dataframe
for index, row in df.iterrows():
    # Get the image_name and question
    image_name = row['image_name']
    question = row['question']
    
    # If image_name is not in the dictionary, add it with count 1
    if image_name not in question_counts:
        question_counts[image_name] = 1
    else:
        # If image_name is already in the dictionary, increment the count
        question_counts[image_name] += 1
    
    # Set the qa_id value for the row
    df.at[index, 'qa_id'] = question_counts[image_name]

# Save the modified dataframe to a new CSV file
df.to_csv('descriptionQuestions.csv', index=False, header=False)
