import matplotlib.pyplot as plt
import pandas as pd
import ast
from datetime import datetime
# Load the files to inspect their content and structure
it_staff_file = 'MB_IT.csv'
all_staff_file = 'MB_cleaned_2.csv'

# Read the CSV files
it_staff_df = pd.read_csv(it_staff_file)
all_staff_df = pd.read_csv(all_staff_file)
# Count the number of IT employees and total employees
it_staff_count = it_staff_df.shape[0]
all_staff_count = all_staff_df.shape[0]

# Calculate non-IT staff
non_it_staff_count = all_staff_count - it_staff_count

# Data for the pie chart
labels = [f'IT Staff ({it_staff_count})', f'Non-IT Staff ({non_it_staff_count})']
sizes = [it_staff_count, non_it_staff_count]

# Create a pie chart
plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Show the chart
plt.title(f'Comparison of IT Staff vs Non-IT Staff at MBBank \n (Total Staff: {all_staff_count})')
plt.savefig('MB.png')
plt.show()

avr_age_it_staff = it_staff_df['estimated_age'].mean()
print(f'The avarage age of MBBank staff is {avr_age_it_staff}')


# Function to calculate the average duration at the current company
def calculate_average_duration(df):
    total_duration = 0
    count = 0
    
    for index, row in df.iterrows():
        experiences = row['experiences']
        # Parse the string to list of dictionaries
        try:
            experiences_list = ast.literal_eval(experiences)
        except:
            continue
        
        # Iterate through the list of experiences
        for experience in experiences_list:
            company = experience.get('company', '')
            if company == 'MBBank' and experience.get('end_date') is None:  # Check if it's current job
                start_date_str = experience.get('start_date')
                if start_date_str:
                    # Convert start date to datetime object
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                    # Calculate duration till now
                    duration = (datetime.now() - start_date).days / 365.25  # Convert to years
                    total_duration += duration
                    count += 1
                break
    
    # Calculate the average
    if count > 0:
        average_duration = total_duration / count
        return average_duration
    else:
        return None

# Calculate average duration for Bank of America employees
average_duration = calculate_average_duration(all_staff_df)

print(f'The average duration of MBBank IT/Analyst employees {average_duration}')