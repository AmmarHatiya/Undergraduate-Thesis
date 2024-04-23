# # # 
# # # Compute Semantic Similarity scores between each generated question and ground truth questions
# # # &
# # # Calculate Precision
# # # 

import os
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.translate import meteor_score
import spacy

# Load the spaCy model with large word vectors
nlp = spacy.load("en_core_web_lg")

# Read the GroundTruth.csv and method.csv files
df_groundtruth = pd.read_csv('Ground Truth/GroundTruth.csv', header=None, names=['id', 'image_name', 'qa_id', 'question', 'answer'])
df_method = pd.read_csv('Results/basePrompt.csv', header=None, names=['id', 'image_name', 'qa_id', 'question', 'answer'])

# Merge the two dataframes on 'image_name'
merged_df = pd.merge(df_groundtruth, df_method, on='image_name', suffixes=('_gt', '_m'))

# Initialize lists to store data for the CSV
data = []

# Iterate over each row in the merged dataframe
for index, row in merged_df.iterrows():
    
    # Calculate METEOR score for the questions
    reference = row['question_gt']
    hypothesis = row['question_m']

    # Process the sentences using spaCy
    ref = nlp(reference)
    hyp = nlp(hypothesis)

    # Calculate the similarity between the two sentences
    similarity_score = ref.similarity(hyp)
    
    # Append data to the list
    data.append({
        'id': row['id_gt'],
        'image_name': row['image_name'],
        'score': similarity_score,
        'gt_qa_id': row['qa_id_gt'],
        'gt_question': row['question_gt'],
        'm_qa_id': row['qa_id_m'],
        'm_question': row['question_m']
    })

# Create a dataframe from the collected data
result_df = pd.DataFrame(data)

# Specify the folder path
folder_path = 'Evaluation/'

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Save the dataframe to a CSV file in the specified folder
result_df.to_csv(os.path.join(folder_path, 'base_Q.csv'), index=False)
# 