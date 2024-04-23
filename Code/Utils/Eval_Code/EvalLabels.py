import pandas as pd
from sklearn.metrics import classification_report

# Load the ground truth and predicted labels from CSV files
ground_truth = pd.read_csv("DiagramLabelsGT.csv", names=["id_gt", "image_name", "image_path", "label_gt"])
predicted_labels_1 = pd.read_csv("GeneratedZeroshotLabels.csv", names=["id_pred", "image_name", "image_path", "label_pred"])
predicted_labels_2 = pd.read_csv("GeneratedOneshotLabels.csv", names=["id_pred", "image_name", "image_path", "label_pred"])

# Merge the ground truth and predicted labels based on image_name
merged_1 = pd.merge(ground_truth, predicted_labels_1, on="image_name", suffixes=('_gt', '_pred'))
merged_2 = pd.merge(ground_truth, predicted_labels_2, on="image_name", suffixes=('_gt', '_pred'))

# Calculate evaluation metrics for each predicted label file
evaluation_metrics_1 = classification_report(merged_1['label_gt'], merged_1['label_pred'], output_dict=True)
evaluation_metrics_2 = classification_report(merged_2['label_gt'], merged_2['label_pred'], output_dict=True)


# Convert evaluation metrics to DataFrame
evaluation_metrics_df_1 = pd.DataFrame(evaluation_metrics_1)
evaluation_metrics_df_2 = pd.DataFrame(evaluation_metrics_2)

# Save the evaluation metrics table to CSV files
evaluation_metrics_df_1.to_csv("zeroshotLabeling.csv", index=True)
evaluation_metrics_df_2.to_csv("oneshotLabeling.csv", index=True)

# Print evaluation metrics tables
print("Evaluation Metrics for 0 Shot Labeling:")
print(evaluation_metrics_df_1)
print("\nEvaluation Metrics for 1 shot Labeling:")
print(evaluation_metrics_df_2)

# Extract precision, recall, and F1-score from the evaluation metrics dictionaries
data = dict(list(evaluation_metrics_1.items())[:3])
precision_1 = [data[label]['precision'] for label in data if 'precision' in data[label]]
recall_1 = [data[label]['recall'] for label in data if 'recall' in data[label]]
f1_score_1 = [data[label]['f1-score'] for label in data if 'f1-score' in data[label]]

data = dict(list(evaluation_metrics_2.items())[:3])
precision_2 = [data[label]['precision'] for label in data if 'precision' in data[label]]
recall_2 = [data[label]['recall'] for label in data if 'recall' in data[label]]
f1_score_2 = [data[label]['f1-score'] for label in data if 'f1-score' in data[label]]

# Plot the metrics
import matplotlib.pyplot as plt

labels = ['Other', 'Item Dictionary', 'Procedural']
x = range(len(labels))

plt.figure(figsize=(10, 6))
bar_width = 0.125

plt.bar(x, precision_1, color='lightblue', width=bar_width, label='Precision (Zero-Shot)')
plt.bar([pos + bar_width for pos in x], precision_2, color='orange', edgecolor='black', linewidth=1.5, width=bar_width, label='Precision (One-Shot)')
plt.bar([pos + 2 * bar_width +0.01 for pos in x], recall_1, color='blue', width=bar_width, label='Recall (Zero-Shot)')
plt.bar([pos + 3 * bar_width for pos in x], recall_2, color='red', edgecolor='black', linewidth=1.5,  width=bar_width, label='Recall (One-Shot)')
plt.bar([pos + 4 * bar_width +0.01 for pos in x], f1_score_1, color='darkblue', width=bar_width, label='F1-score (Zero-Shot)')
plt.bar([pos + 5 * bar_width for pos in x], f1_score_2, edgecolor='black', linewidth=1.5, color='darkred', width=bar_width, label='F1-score (One-Shot)')

plt.xlabel('Labels')
plt.ylabel('Scores')
plt.title('Label Generation Evaluation by Label and Learning Method')
plt.xticks([pos + 2.5 * bar_width for pos in x], labels)
plt.legend()
plt.tight_layout()
plt.savefig('label_generation_eval_plot.png')

