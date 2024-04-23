# Calculate F1 score for a method Q, A and Pair files (using precision and recall files)
import pandas as pd

# Function to calculate F1 score
def calculate_f1_score(precision, recall):
    # Calculate F1 score element-wise
    f1_score = 2 * ((precision * recall) / (precision + recall))
    # Handle cases where precision and recall are both zero
    f1_score = f1_score.fillna(0)
    return f1_score


# Function to process a pair of precision and recall files and generate F1 score
def generate_f1_score(precision_file, recall_file, output_file):
    # Read precision and recall files
    precision_df = pd.read_csv(precision_file)
    recall_df = pd.read_csv(recall_file)
    
    # Merge precision and recall dataframes on 'image_name'
    merged_df = pd.merge(precision_df, recall_df, on='image_name', suffixes=('_precision', '_recall'))
    
    # Calculate F1 score
    merged_df['f1_score'] = calculate_f1_score(merged_df['precision'], merged_df['recall'])
    # Save F1 score dataframe to a CSV file
    merged_df.to_csv(output_file, columns=['image_name', 'f1_score', 'id_recall'], index=False)

output_directory = 'Evaluation/Meteor/1.0 Base Prompt/'
file_prefix = '1_0_base'  
folder_path= output_directory+file_prefix
   
# Paths to precision and recall files and output directory
precision_files = [
    # folder_path+'_precision_Q.csv',
    #                folder_path+'_precision_A.csv',
                   folder_path+'_precision_Pair.csv'
                  ]

recall_files = [
    # folder_path+'_recall_Q.csv',
    #             folder_path+'_recall_A.csv',
                folder_path+'_recall_Pair.csv'
               ]


# Generate F1 score for each pair
for precision_file, recall_file in zip(precision_files, recall_files):
    pair_name = precision_file.split('_')[-1].split('.')[0]  # Extract pair identifier from filename
    output_file = f'{folder_path}_f1_{pair_name}.csv'
    generate_f1_score(precision_file, recall_file, output_file)

print("F1 scores calculated and saved successfully.")
