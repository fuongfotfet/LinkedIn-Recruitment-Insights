import pandas as pd
import numpy as np 

deloitte_data = pd.read_csv('MBBank.csv')

# Keeping only the relevant columns as per the previous processes
deloitte_columns_to_keep = [
    'name', 'headline', 'estimated_age', 'current_position', 'current_company', 
    'top_skill_1', 'top_skill_2', 'top_skill_3', 'experiences'
]

# Check if the columns exist in the dataset and filter
deloitte_filtered_data = deloitte_data[[col for col in deloitte_columns_to_keep if col in deloitte_data.columns]]

# Now filtering only for 'Deloitte' in 'current_company' and 'headline'
deloitte_filtered_data_deloitte = deloitte_filtered_data[
    deloitte_filtered_data['current_company'].str.contains('MB', na=False) |
    deloitte_filtered_data['headline'].str.contains('MB', na=False)
]

# Removing duplicates
deloitte_filtered_data_no_duplicates = deloitte_filtered_data_deloitte.drop_duplicates()

# Move 'LinkedIn Member' to the end
linkedin_members_deloitte = deloitte_filtered_data_no_duplicates[deloitte_filtered_data_no_duplicates['name'] == 'LinkedIn Member']
non_linkedin_members_deloitte = deloitte_filtered_data_no_duplicates[deloitte_filtered_data_no_duplicates['name'] != 'LinkedIn Member']

# Concatenating to move LinkedIn Members to the end
deloitte_ordered_data = pd.concat([non_linkedin_members_deloitte, linkedin_members_deloitte], ignore_index=True)

# Exporting the cleaned Deloitte data to a CSV file
deloitte_ordered_data.to_csv('MB_cleaned.csv', index=False)
