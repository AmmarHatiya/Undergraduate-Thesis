# Merge Ground Truth from 3 categories into 1 file
import pandas as pd

# Define column names
columns = ['id', 'image_name', 'qa_id', 'question', 'answer']

# Read the CSV files without header rows
df_diagram = pd.read_csv('category_other_w_example.csv', names=columns)
df_procedural = pd.read_csv('category_procedural_w_example.csv', names=columns)
df_itemdict = pd.read_csv('category_itemdict_w_example.csv', names=columns)

# Concatenate the DataFrames
frames = [df_diagram, df_procedural, df_itemdict]
df_merged = pd.concat(frames)

# Reset the index of the merged DataFrame
df_merged.reset_index(drop=True, inplace=True)

# Initialize a dictionary to store the mapping of image_name to id
image_name_to_id = {}

# Initialize the id counter
id_counter = 1

# Iterate through the merged DataFrame
for index, row in df_merged.iterrows():
    image_name = row['image_name']
    # If the image_name is not in the dictionary, assign it a new id
    if image_name not in image_name_to_id:
        image_name_to_id[image_name] = id_counter
        id_counter += 1
    # Assign the id to the row
    df_merged.at[index, 'id'] = image_name_to_id[image_name]

# Convert the 'id' column to integer
df_merged['id'] = df_merged['id'].astype(int)

# Reorder the columns with 'id' as the first column
df_merged = df_merged[['id', 'image_name', 'qa_id', 'question', 'answer']]

# Save the merged DataFrame to a CSV file
df_merged.to_csv('prompt_allCategorical.csv', index=False)

