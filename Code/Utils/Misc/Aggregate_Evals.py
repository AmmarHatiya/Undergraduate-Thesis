# Aggregate the precision, recall, and F1 scores into 1 file for each method (1 for Questions, 1 for Answers, 1 for QA Pair)
# suffix: Q, A or Pair
# folder_path, fileName: Meteor or Semantic Similarity

import os
import pandas as pd

suffix = "_Q"
folder_path = "Meteor/Meteor"+suffix+"/"
fileName = "Meteor_Stats"+suffix
# Define the folder path
folder_path = "Evaluation/"+folder_path

# Dictionary to map CSV files to method names
method_files = {
    "1shot_eval"+suffix+".csv": "1-Shot",
    "2shot_eval"+suffix+".csv": "2-Shot",
    "base_eval"+suffix+".csv": "Vanilla",
    "categorical_eval"+suffix+".csv": "1-Shot + Categorization",
    "description_eval"+suffix+".csv": "Seq2seq w/SRL"
}

# Initialize an empty dataframe to store the aggregated results
agg_df = pd.DataFrame(columns=['method', 'precision', 'recall', 'f1_score', 'id'])

# Iterate over method files
for file_name, method_name in method_files.items():
    file_path = os.path.join(folder_path, file_name)
    
    if os.path.isfile(file_path):
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Calculate average metrics
        avg_metrics = df[['precision', 'recall', 'f1_score']].mean().to_frame().T
        avg_metrics['method'] = method_name
        avg_metrics['id'] = df['id'].nunique()  # Count unique image_names
        agg_df = pd.concat([agg_df, avg_metrics], ignore_index=True)

# Save the aggregated results to a CSV file
agg_df.to_csv(fileName+".csv", index=False)

print("Averaged metrics saved successfully.")