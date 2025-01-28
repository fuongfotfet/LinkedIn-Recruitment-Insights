import pandas as pd
import numpy as np

df = pd.read_csv("Deloitte_cleaned_2.csv")
it_keywords = ['developer', 'engineer', 'IT', 'software', 'data', 'intelligence', 'analyst', 'scientist', 'software', 'AI', "cybersecurity", 'security']

# Filter rows containing the keywords in either the 'headline' or 'current_position' columns
employee_count_if = 0

# Loop through each row and check for the keywords in the 'headline' and 'current_position' columns
for index, row in df.iterrows():
    if any(keyword in str(row['current_position']).lower() for keyword in it_keywords):
        employee_count_if += 1
filtered_it_data_df = df[
    df.apply(lambda row:  any(keyword in str(row['current_position']).lower() for keyword in it_keywords), axis=1)]
print(employee_count_if)
filtered_it_data_df.to_csv('Deloitte_IT.csv', index = False)
