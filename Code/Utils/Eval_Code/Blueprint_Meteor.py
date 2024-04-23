# # # 
# # # Compute METEOR scores between each generated question and ground truth questions
# # # &
# # # Calculate Precision
# # #

import os
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.translate import meteor_score

# Read the GroundTruth.csv and method.csv files
df_groundtruth = pd.read_csv('Ground Truth/GroundTruth.csv', header=None, names=['id_gt', 'image_name', 'qa_id_gt', 'question_gt', 'answer_gt'])
df_method = pd.read_csv('Results/Example based/prompt_w_example.csv', header=None, names=['id_m', 'image_name', 'qa_id_m', 'question_m', 'answer_m'])

save_file_name = '1shot'
# Specify the folder path to save the METEOR CSV file
folder_path = 'Evaluation/Meteor/1.1.1 1-Shot'


os.makedirs(folder_path, exist_ok=True)

# Merge the two dataframes on 'image_name'
merged_df = pd.merge(df_groundtruth, df_method, on='image_name', suffixes=('_gt', '_m'))

# Initialize lists to store data for the METEOR CSV
meteor_data = []
meteor_scores_dict = {}

# Iterate over each row in the merged dataframe
for index, row in merged_df.iterrows():
    # Calculate METEOR score for the questions
    reference_tokens = word_tokenize(row['question_gt'])
    candidate_tokens = word_tokenize(row['question_m'])
    pair_key = (row['question_gt'], row['question_m'])

    # Check if METEOR score for this pair has been computed before
    if pair_key in meteor_scores_dict:
        meteor = meteor_scores_dict[pair_key]
    else:
        meteor = meteor_score.single_meteor_score(reference_tokens, candidate_tokens)
        meteor_scores_dict[pair_key] = meteor
    
    # Append METEOR score data to the list
    meteor_data.append({
        'id': row['id_gt'],
        'image_name': row['image_name'],
        'score': meteor,
        'gt_qa_id': row['qa_id_gt'],
        'gt_question': row['question_gt'],
        'm_qa_id': row['qa_id_m'],
        'm_question': row['question_m']
    })

# Create a dataframe from the collected METEOR data
meteor_df = pd.DataFrame(meteor_data)

# Save the METEOR dataframe to a CSV file
meteor_df.to_csv(os.path.join(folder_path, save_file_name+'_Q.csv'), index=False)

precision_dict = {}

# Iterate over unique image_names
for image_name in merged_df['image_name'].unique():
    # Filter rows by the current image_name
    image_rows = merged_df[merged_df['image_name'] == image_name]
    meteor_scores = []

    # Iterate over method questions for the current image_name
    for _, method_row in image_rows.iterrows():
        method_question = method_row['question_m']
        max_meteor_score = 0

        # Compare method question with all ground truth questions for the current image_name
        for _, gt_row in image_rows.iterrows():
            reference_tokens = word_tokenize(gt_row['question_gt'])
            hypothesis_tokens = word_tokenize(method_question)
            pair_key = (gt_row['question_gt'], method_question)

            # Check if METEOR score for this pair has been computed before
            if pair_key in meteor_scores_dict:
                meteor_score_val = meteor_scores_dict[pair_key]
            else:
                meteor_score_val = meteor_score.single_meteor_score(reference_tokens, hypothesis_tokens)
                meteor_scores_dict[pair_key] = meteor_score_val
            
            max_meteor_score = max(max_meteor_score, meteor_score_val)

        # Store the maximum METEOR score for the current method question
        meteor_scores.append(max_meteor_score)
    
    # Calculate precision as the average of maximum METEOR scores for all method questions
    precision_dict[image_name] = sum(meteor_scores) / len(meteor_scores)

# Create dataframe from precision dictionary
precision_df = pd.DataFrame(precision_dict.items(), columns=['image_name', 'precision'])

# Calculate unique image_name count
precision_df['id'] = range(1, len(precision_df) + 1)

# Save the precision dataframe to a CSV file
precision_df.to_csv(os.path.join(folder_path, 'precision_Q.csv'), index=False)










# 
# GENERATE SCORES + PRECISION FOR ANSWERS
# 



# Initialize lists to store data for the METEOR CSV
meteor_data = []
meteor_scores_dict = {}

# Iterate over each row in the merged dataframe
for index, row in merged_df.iterrows():
    # Calculate METEOR score for the answer
    reference_tokens = word_tokenize(row['answer_gt'])
    candidate_tokens = word_tokenize(row['answer_m'])
    pair_key = (row['answer_gt'], row['answer_m'])

    # Check if METEOR score for this pair has been computed before
    if pair_key in meteor_scores_dict:
        meteor = meteor_scores_dict[pair_key]
    else:
        meteor = meteor_score.single_meteor_score(reference_tokens, candidate_tokens)
        meteor_scores_dict[pair_key] = meteor
    
    # Append METEOR score data to the list
    meteor_data.append({
        'id': row['id_gt'],
        'image_name': row['image_name'],
        'score': meteor,
        'gt_qa_id': row['qa_id_gt'],
        'gt_answer': row['answer_gt'],
        'm_qa_id': row['qa_id_m'],
        'm_answer': row['answer_m']
    })

# Create a dataframe from the collected METEOR data
meteor_df = pd.DataFrame(meteor_data)

# Save the METEOR dataframe to a CSV file
meteor_df.to_csv(os.path.join(folder_path, save_file_name+'_A.csv'), index=False)

precision_dict = {}

# Iterate over unique image_names
for image_name in merged_df['image_name'].unique():
    # Filter rows by the current image_name
    image_rows = merged_df[merged_df['image_name'] == image_name]
    meteor_scores = []

    # Iterate over method answer for the current image_name
    for _, method_row in image_rows.iterrows():
        method_answer = method_row['answer_m']
        max_meteor_score = 0

        # Compare method answers with all ground truth answers for the current image_name
        for _, gt_row in image_rows.iterrows():
            reference_tokens = word_tokenize(gt_row['answer_gt'])
            hypothesis_tokens = word_tokenize(method_answer)
            pair_key = (gt_row['answer_gt'], method_answer)

            # Check if METEOR score for this pair has been computed before
            if pair_key in meteor_scores_dict:
                meteor_score_val = meteor_scores_dict[pair_key]
            else:
                meteor_score_val = meteor_score.single_meteor_score(reference_tokens, hypothesis_tokens)
                meteor_scores_dict[pair_key] = meteor_score_val
            
            max_meteor_score = max(max_meteor_score, meteor_score_val)

        # Store the maximum METEOR score for the current method answer
        meteor_scores.append(max_meteor_score)
    
    # Calculate precision as the average of maximum METEOR scores for all method answers
    precision_dict[image_name] = sum(meteor_scores) / len(meteor_scores)

# Create dataframe from precision dictionary
precision_df = pd.DataFrame(precision_dict.items(), columns=['image_name', 'precision'])

# Calculate unique image_name count
precision_df['id'] = range(1, len(precision_df) + 1)

# Save the precision dataframe to a CSV file
precision_df.to_csv(os.path.join(folder_path, 'precision_A.csv'), index=False)
