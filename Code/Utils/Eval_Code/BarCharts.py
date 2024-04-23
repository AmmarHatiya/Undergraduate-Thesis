# # # 
# # # Generate Bar charts 
# # #

import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the folder path
score_name = "Meteor"
scorename = "Meteor"
folder_path = "Evaluation/Meteor/"
metrics = ['precision', 'recall', 'f1_score']
subfolder_modelName = {score_name+"_Q":"Questions", score_name+"_A":"Answers", score_name+"_Pair":"Q&A Pairs"}

target_folders = [score_name+"_Q", score_name+"_A", score_name+"_Pair"]

# Function to aggregate CSV files in a subfolder
def aggregate_csv(subfolder):
    # Dictionary to map CSV files to model names
    model_files = {
        "1shot_eval": "1-Shot P.E",
        "2shot_eval": "2-Shot P.E",
        "base_eval": "Vanilla P.E",
        "categorical_eval": "1-Shot + Categorization P.E"
    }
    
    # Get the suffix from the subfolder name (2: for Semantic Similarity, 1: for Meteor)
    suffix = subfolder.split('_')[1]
    
    # Initialize empty dataframes
    avg_df = pd.DataFrame(columns=['model', 'precision_avg', 'recall_avg', 'f1_score_avg'])
    min_df = pd.DataFrame(columns=['model', 'precision_min', 'recall_min', 'f1_score_min'])
    
    # Iterate over model files
    for file_prefix, model_name in model_files.items():
        file_path = os.path.join(folder_path, subfolder, f"{file_prefix}_{suffix}.csv")

        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            # Calculate average metrics
            avg_metrics = df[['precision', 'recall', 'f1_score']].mean().to_frame().T
            avg_metrics['model'] = model_name
            avg_metrics.columns = ['precision_avg', 'recall_avg', 'f1_score_avg', 'model']  # Set column names
            avg_df = pd.concat([avg_df, avg_metrics], ignore_index=True)
            
            # Calculate minimum metrics
            min_metrics = df[['precision', 'recall', 'f1_score']].min().to_frame().T
            min_metrics['model'] = model_name
            min_metrics.columns = ['precision_min', 'recall_min', 'f1_score_min', 'model']  # Set column names
            min_df = pd.concat([min_df, min_metrics], ignore_index=True)
            
    # Include "Description" model only for Semantic_Similarity_Q subfolder
    if subfolder == score_name+"_Q":
        description_file_path = os.path.join(folder_path, subfolder, "description_eval_Q.csv")
        if os.path.isfile(description_file_path):
            description_df = pd.read_csv(description_file_path)
            description_avg_metrics = description_df[['precision', 'recall', 'f1_score']].mean().to_frame().T
            description_avg_metrics['model'] = "Seq2Seq (w/ SRL)"
            description_avg_metrics.columns = ['precision_avg', 'recall_avg', 'f1_score_avg', 'model']  # Set column names
            avg_df = pd.concat([avg_df, description_avg_metrics], ignore_index=True)
                    
            description_min_metrics = description_df[['precision', 'recall', 'f1_score']].min().to_frame().T
            description_min_metrics['model'] = "Seq2Seq (w/ SRL)"
            description_min_metrics.columns = ['precision_min', 'recall_min', 'f1_score_min', 'model']  # Set column names
            min_df = pd.concat([min_df, description_min_metrics], ignore_index=True)
                
    return avg_df, min_df

# Iterate over target folders and generate bar charts
for subfolder in target_folders:
    avg_df, min_df = aggregate_csv(subfolder)
    subfolder_path = os.path.join(folder_path, subfolder)
    
    # Plot bar charts for each metric
    for metric in metrics:
        plt.figure(figsize=(10, 6))

        # Calculate the position for the bars
        x = range(len(avg_df['model']))  # X positions for each model
        width = 0.35  # Width of each bar
        offset = width / 2  # Offset to position the bars

        # Plot average metrics
        plt.bar([pos - offset for pos in x], avg_df[f'{metric}_avg'], width, color='blue', alpha=0.5, label='Average')

        # Plot minimum metrics
        plt.bar([pos + offset for pos in x], min_df[f'{metric}_min'], width, color='orange', alpha=0.5, label='Minimum')

        # Add labels and title
        plt.xlabel('Model')
        plt.ylabel(metric.capitalize())
        plt.title(f'{scorename} {metric.capitalize()} Comparison for {subfolder_modelName[subfolder]}')
        plt.xticks(x, avg_df['model'], rotation=12)
        plt.legend()

        # Set y-axis limits based on the maximum and minimum values of the metrics
        min_value = min(avg_df[f'{metric}_avg'].min(), min_df[f'{metric}_min'].min())
        max_value = max(avg_df[f'{metric}_avg'].max(), min_df[f'{metric}_min'].max())
        plt.ylim(min_value - 0.01, max_value + 0.01)  # Add a buffer for better visualization

        # Save the plot
        plt.savefig(os.path.join(subfolder_path, f'{metric}_comparison.png'))
        plt.close()

print("Bar charts generated and saved successfully.")