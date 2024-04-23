import pandas as pd
from nltk.translate.bleu_score import sentence_bleu
import os 

# Read the GroundTruth.csv and method.csv files
df_groundtruth = pd.read_csv('Ground Truth/GroundTruth.csv', header=None, names=['id', 'image_name', 'qa_id', 'question', 'answer'])
df_method = pd.read_csv('Results/Description based/descriptionQuestions.csv', header=None, names=['id', 'image_name', 'description', 'sentence_srl', 'sentence', 'question', 'qa_id'])

# Specify the folder path
folder_path = 'Evaluation/Bleu/1.3 Description based'

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Merge the two dataframes on 'image_name'
merged_df = pd.merge(df_groundtruth, df_method, on='image_name', suffixes=('_gt', '_m'))

# Initialize lists to store data for the CSV
data = []

# Iterate over each row in the merged dataframe
for index, row in merged_df.iterrows():
    # Calculate BLEU score for the questions
    reference = row['question_gt'].split()
    hypothesis = row['question_m'].split()
    bleu_score = sentence_bleu([reference], hypothesis)
    
    # Append data to the list
    data.append({
        'id': row['id_gt'],
        'image_name': row['image_name'],
        'score': bleu_score,
        'gt_qa_id': row['qa_id_gt'],
        'gt_question': row['question_gt'],
        'm_qa_id': row['qa_id_m'],
        'm_question': row['question_m']
    })

# Create a dataframe from the collected data
result_df = pd.DataFrame(data)

# Save the dataframe to a CSV file in the specified folder
result_df.to_csv(os.path.join(folder_path, 'description_Q.csv'), index=False)





# 
# GENERATE SCORES FROM ANSWERS
# 


# # Initialize lists to store data for the CSV
# data = []

# # Iterate over each row in the merged dataframe
# for index, row in merged_df.iterrows():
#     # Calculate BLEU score for the questions
#     reference = row['answer_gt'].split()
#     hypothesis = row['answer_m'].split()
#     bleu_score = sentence_bleu([reference], hypothesis)
    
#     # Append data to the list
#     data.append({
#         'id': row['id_gt'],
#         'image_name': row['image_name'],
#         'score': bleu_score,
#         'gt_qa_id': row['qa_id_gt'],
#         'gt_question': row['answer_gt'],
#         'm_qa_id': row['qa_id_m'],
#         'm_question': row['answer_m']
#     })

# # Create a dataframe from the collected data
# result_df = pd.DataFrame(data)

# # Save the dataframe to a CSV file in the specified folder
# result_df.to_csv(os.path.join(folder_path, 'categorical_A.csv'), index=False)
