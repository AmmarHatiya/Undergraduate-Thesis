# Evaluation of the Labeling/Categorization of Images Results
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

# Define file paths
gt_file = "csv/labeling/DiagramLabelsGT.csv"
oneshot_file = "csv/labeling/GeneratedOneshotLabels.csv"
zeroshot_file = "csv/labeling/GeneratedZeroshotLabels.csv"

# Load data into pandas dataframes
gt_df = pd.read_csv(gt_file, header=None, names=["id", "image_name", "image_path", "Label"])
oneshot_df = pd.read_csv(oneshot_file, header=None, names=["id", "image_name", "image_path", "Label"])
zeroshot_df = pd.read_csv(zeroshot_file, header=None, names=["id", "image_name", "image_path", "Label"])

# Define labels
labels = ["Diagram-Other", "Diagram-ItemDictionary", "Diagram-Procedural"]

# Calculate evaluation metrics for 1-Shot labels
oneshot_metrics = precision_recall_fscore_support(gt_df["Label"], oneshot_df["Label"], labels=labels, average="macro")
oneshot_precision, oneshot_recall, oneshot_f1, _ = oneshot_metrics
oneshot_accuracy = accuracy_score(gt_df["Label"], oneshot_df["Label"])

# Calculate evaluation metrics for Zero-Shot labels
zeroshot_metrics = precision_recall_fscore_support(gt_df["Label"], zeroshot_df["Label"], labels=labels, average="macro")
zeroshot_precision, zeroshot_recall, zeroshot_f1, _ = zeroshot_metrics
zeroshot_accuracy = accuracy_score(gt_df["Label"], zeroshot_df["Label"])

# Create dataframe for evaluation results
eval_results = pd.DataFrame({
    "Model": ["1-Shot", "Zero-Shot"],
    "Precision": [oneshot_precision, zeroshot_precision],
    "Recall": [oneshot_recall, zeroshot_recall],
    "F1 Score": [oneshot_f1, zeroshot_f1],
    "Accuracy": [oneshot_accuracy, zeroshot_accuracy]
})

# Save evaluation results to CSV files
eval_1shot_file = "csv/labeling/Eval_1ShotLabel.csv"
eval_0shot_file = "csv/labeling/Eval_0ShotLabel.csv"
eval_results.to_csv(eval_1shot_file, index=False)
eval_results.to_csv(eval_0shot_file, index=False)

print("Evaluation results saved successfully.")
