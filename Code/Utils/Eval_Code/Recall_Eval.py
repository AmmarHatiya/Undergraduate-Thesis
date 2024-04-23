# This file computes the recall for questions, answers, and QA pairs (average)

import pandas as pd
import os


# Specify the folder path to save the recall CSV file
folder_path = 'Evaluation/Meteor/1.0 Base Prompt'
save_file_name = '1_0_base'

# # # 
# # # GENERATE QUESTION recall
# # # 
# Read the semantic similarity CSV file
sem_similarity_df = pd.read_csv(folder_path+'/'+save_file_name+'_Q.csv')

os.makedirs(folder_path, exist_ok=True)

# Initialize a dictionary to store recall values
recall_dict = {}

# Iterate over unique image_names
for image_name in sem_similarity_df['image_name'].unique():
    # Filter rows by the current image_name
    image_rows = sem_similarity_df[sem_similarity_df['image_name'] == image_name]
    
    # Initialize a dictionary to store max semantic similarity scores for each gt_qa_id
    max_sem_similarity_scores = {}
    
    # Iterate over each row for the current image_name
    for _, row in image_rows.iterrows():
        gt_qa_id = row['gt_qa_id']
        score = row['score']
        
        # Update max score for the current gt_qa_id
        if gt_qa_id in max_sem_similarity_scores:
            max_sem_similarity_scores[gt_qa_id] = max(max_sem_similarity_scores[gt_qa_id], score)
        else:
            max_sem_similarity_scores[gt_qa_id] = score
    
    # Calculate recall as the average of maximum semantic similarity scores for all ground truth questions
    recall_dict[image_name] = sum(max_sem_similarity_scores.values()) / len(max_sem_similarity_scores)

# Create dataframe from recall dictionary
recall_df = pd.DataFrame(recall_dict.items(), columns=['image_name', 'recall'])

# Calculate unique image_name count
recall_df['id'] = range(1, len(recall_df) + 1)

# Save the recall dataframe to a CSV file
recall_df.to_csv(os.path.join(folder_path, save_file_name + '_recall_Q.csv'), index=False)




# # # 
# # # GENERATE ANSWER recall
# # # 
# Read the semantic similarity CSV file
sem_similarity_df = pd.read_csv(folder_path+'/'+save_file_name+'_A.csv')


# Initialize a dictionary to store recall values
recall_dict = {}

# Iterate over unique image_names
for image_name in sem_similarity_df['image_name'].unique():
    # Filter rows by the current image_name
    image_rows = sem_similarity_df[sem_similarity_df['image_name'] == image_name]
    
    # Initialize a dictionary to store max semantic similarity scores for each gt_qa_id
    max_sem_similarity_scores = {}
    
    # Iterate over each row for the current image_name
    for _, row in image_rows.iterrows():
        gt_qa_id = row['gt_qa_id']
        score = row['score']
        
        # Update max score for the current gt_qa_id
        if gt_qa_id in max_sem_similarity_scores:
            max_sem_similarity_scores[gt_qa_id] = max(max_sem_similarity_scores[gt_qa_id], score)
        else:
            max_sem_similarity_scores[gt_qa_id] = score
    
    # Calculate recall as the average of maximum semantic similarity scores for all ground truth questions
    recall_dict[image_name] = sum(max_sem_similarity_scores.values()) / len(max_sem_similarity_scores)

# Create dataframe from recall dictionary
recall_df = pd.DataFrame(recall_dict.items(), columns=['image_name', 'recall'])

# Calculate unique image_name count
recall_df['id'] = range(1, len(recall_df) + 1)

# Save the recall dataframe to a CSV file
recall_df.to_csv(os.path.join(folder_path, save_file_name + '_recall_A.csv'), index=False)





# # 
# # GENERATE PAIR recall
# # 
# Read the semantic similarity CSV file
sem_similarity_df = pd.read_csv(folder_path+'/'+save_file_name+'_Pair.csv')


# Initialize a dictionary to store recall values
recall_dict = {}

# Iterate over unique image_names
for image_name in sem_similarity_df['image_name'].unique():
    # Filter rows by the current image_name
    image_rows = sem_similarity_df[sem_similarity_df['image_name'] == image_name]
    
    # Initialize a dictionary to store max semantic similarity scores for each gt_qa_id
    max_sem_similarity_scores = {}
    
    # Iterate over each row for the current image_name
    for _, row in image_rows.iterrows():
        gt_qa_id = row['gt_qa_id']
        score = row['score']
        
        # Update max score for the current gt_qa_id
        if gt_qa_id in max_sem_similarity_scores:
            max_sem_similarity_scores[gt_qa_id] = max(max_sem_similarity_scores[gt_qa_id], score)
        else:
            max_sem_similarity_scores[gt_qa_id] = score
    
    # Calculate recall as the average of maximum semantic similarity scores for all ground truth questions
    recall_dict[image_name] = sum(max_sem_similarity_scores.values()) / len(max_sem_similarity_scores)

# Create dataframe from recall dictionary
recall_df = pd.DataFrame(recall_dict.items(), columns=['image_name', 'recall'])

# Calculate unique image_name count
recall_df['id'] = range(1, len(recall_df) + 1)

# Save the recall dataframe to a CSV file
recall_df.to_csv(os.path.join(folder_path, save_file_name + '_recall_Pair.csv'), index=False)
