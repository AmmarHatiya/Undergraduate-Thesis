import pandas as pd

# Read the CSV file
df = pd.read_csv("text_based_Results.csv", sep=',', skipinitialspace=True)

# Remove duplicate rows based on the generated_question column
df.drop_duplicates(subset=['generated_question'], inplace=True)

# Save the cleaned data to a new CSV file
df.to_csv("cleaned_file.csv", index=False)
