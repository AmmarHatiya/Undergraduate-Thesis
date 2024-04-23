import os
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.translate import meteor_score

# Read the GroundTruth.csv and method.csv files
df_groundtruth = pd.read_csv('Ground Truth/GroundTruth.csv', header=None, names=['id', 'image_name', 'qa_id', 'question', 'answer'])
df_method = pd.read_csv('Results/Description based/descriptionQuestions.csv', header=None, names=['id', 'image_name', 'description', 'sentence_srl', 'sentence', 'question', 'qa_id'])

# Merge the two dataframes on 'image_name'
merged_df = pd.merge(df_groundtruth, df_method, on='image_name', suffixes=('_gt', '_m'))

# Initialize lists to store data for the CSV
data = []


# 
#  GENERATE SCORE FROM QUESTIONS
# 

# Iterate over each row in the merged dataframe
for index, row in merged_df.iterrows():
    
    # Calculate METEOR score for the questions
    reference = row['question_gt']
    hypothesis = row['question_m']

    # Tokenize sentences
    reference_tokens = word_tokenize(reference)
    candidate_tokens = word_tokenize(hypothesis)

    # Compute the METEOR score
    meteor = meteor_score.single_meteor_score(reference_tokens, candidate_tokens)
    
    # Append data to the list
    data.append({
        'id': row['id_gt'],
        'image_name': row['image_name'],
        'score': meteor,
        'gt_qa_id': row['qa_id_gt'],
        'gt_question': row['question_gt'],
        'm_qa_id': row['qa_id_m'],
        'm_question': row['question_m']
    })

# Create a dataframe from the collected data
result_df = pd.DataFrame(data)

# Specify the folder path
folder_path = 'Evaluation/Meteor/1.3 Description based'

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Save the dataframe to a CSV file in the specified folder
result_df.to_csv(os.path.join(folder_path, 'descriptionBased_Q.csv'), index=False)
#