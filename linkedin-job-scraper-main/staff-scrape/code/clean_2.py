import pandas as pd

# Load the uploaded CSV file
file_path = 'MB_cleaned.csv'
df = pd.read_csv(file_path)

import re

# Update the function to handle cases where job title is followed by "at", "|", "@", or "- [Company]"
def extract_job_title_with_variations(headline):
    if isinstance(headline, str):  # Kiểm tra xem giá trị có phải là chuỗi không
        match = re.search(r'^(.*?)(?:\s+at|\s*\||\s+@|\s+-)', headline)
        if match:
            return match.group(1).strip()
        return headline
    return None  # Trả về None nếu không tìm thấy hoặc không phải là chuỗi


# Apply the updated function to extract job titles from 'headline' column
df['extracted_position'] = df['headline'].apply(extract_job_title_with_variations)

# Fill missing values in the 'current_position' column using the extracted job titles
df['current_position'].fillna(df['extracted_position'], inplace=True)

# Drop the temporary 'extracted_position' column
df.drop(columns=['extracted_position'], inplace=True)

# Remove rows where 'current_position' contains the word "Deloitte"
df_filtered = df[~df['current_position'].str.contains("MB", case=False, na=False)]

# Save the updated dataframe to a new file
df_filtered.to_csv('MB_cleaned_2.csv', index=False)