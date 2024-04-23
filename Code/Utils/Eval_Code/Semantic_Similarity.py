import csv
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_md")

# Function to compute similarity score between two sentences
def compute_similarity(sentence1, sentence2):
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)
    return doc1.similarity(doc2)

# Read method.csv and store its contents in memory
method_data = {}
with open("method.csv", newline='') as method_file:
    reader = csv.DictReader(method_file)
    for row in reader:
        image_name = row['image_name']
        if image_name not in method_data:
            method_data[image_name] = []
        method_data[image_name].append(row)

# Read ground_truth.csv and compute similarity scores
eval_data = []
with open("ground_truth.csv", newline='') as ground_truth_file:
    reader = csv.DictReader(ground_truth_file)
    for row in reader:
        image_name = row['image_name']
        if image_name in method_data:
            method_rows = method_data[image_name]
            for method_row in method_rows:
                similarity_score = compute_similarity(row['question'], method_row['question'])
                eval_data.append({
                    'image_name': image_name,
                    'gt_question': row['question'],
                    'qa_id': method_row['qa_id'],
                    'question': method_row['question'],
                    'similarity_score': similarity_score
                })

# Write the computed similarity scores to eval.csv
with open("eval.csv", 'w', newline='') as eval_file:
    fieldnames = ['image_name', 'gt_question', 'qa_id', 'question', 'similarity_score']
    writer = csv.DictWriter(eval_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in eval_data:
        writer.writerow(row)

print("Evaluation scores computed and saved to eval.csv")
