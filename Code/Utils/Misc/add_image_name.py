# 
# This file will go add image_id and image_name from descriptions.csv to the appropriate rows in text_based_Results.csv
# 

import pandas as pd
from difflib import SequenceMatcher

# Function to find the most similar description in descriptions.csv
def find_matching_description(target_description, descriptions_df, cache):
    if target_description in cache:
        return cache[target_description]
    similarities = []
    for description in descriptions_df['description']:
        similarity = SequenceMatcher(None, target_description, description).ratio()
        similarities.append(similarity)
    max_similarity_index = similarities.index(max(similarities))
    image_id = descriptions_df.iloc[max_similarity_index]['image_id']
    image_name = descriptions_df.iloc[max_similarity_index]['image_name']
    cache[target_description] = (image_id, image_name)
    return image_id, image_name

# Load descriptions.csv and text_based_Results.csv
descriptions_df = pd.read_csv("descriptions.csv")
results_df = pd.read_csv("text_based_Results.csv")

# Create a dictionary to store already found image_id and image_name pairs
cache = {}

# Create a new DataFrame to store formatted data
formatted_df = pd.DataFrame(columns=['image_id', 'image_name', 'description', 'sentence_srl', 'sentence', 'generated_question'])

# Iterate over each row in text_based_Results.csv
for index, row in results_df.iterrows():
    description = row['description']
    # Find the most similar description in descriptions.csv
    image_id, image_name = find_matching_description(description, descriptions_df, cache)
    # Add the data to the new DataFrame
    formatted_df = formatted_df._append({'image_id': image_id,
                                        'image_name': image_name,
                                        'description': description,
                                        'sentence_srl': row['sentence_srl'],
                                        'sentence': row['sentence'],
                                        'generated_question': row['generated_question']}, ignore_index=True)
    print("Looking for:", description[:40]) 

# Save the formatted data to formatted.csv
formatted_df.to_csv("formatted.csv", index=False)

