import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the datasets
deloitte = pd.read_csv('Deloitte_IT.csv')
mb_bank = pd.read_csv('MB_IT.csv')
boa = pd.read_csv('BOA_IT.csv')
vcb = pd.read_csv('Vietcombank_IT.csv')

# Extract top skills from each dataset
skills_deloitte = deloitte[['top_skill_1', 'top_skill_2', 'top_skill_3']].fillna('').values.flatten()
skills_mb = mb_bank[['top_skill_1', 'top_skill_2', 'top_skill_3']].fillna('').values.flatten()
skills_boa = boa[['top_skill_1', 'top_skill_2', 'top_skill_3']].fillna('').values.flatten()
skills_vcb = vcb[['top_skill_1', 'top_skill_2', 'top_skill_3']].fillna('').values.flatten()
# Combine all skills into one list
all_skills = list(skills_deloitte) + list(skills_mb) + list(skills_boa)

# Convert list to a single string for word cloud
skills_text = ' '.join(all_skills)
skills_vcb_text = ' '.join(skills_vcb)
# Generate a word cloud image
wordcloud = WordCloud(width = 800, height = 400, background_color ='white').generate(skills_text)
wordcloud_2 = WordCloud(width = 800, height = 400, background_color ='white').generate(skills_vcb_text)
# Display the word cloud image
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('skills.png')
plt.show()

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud_2, interpolation='bilinear')
plt.axis("off")
plt.savefig('skills_VCB.png')
plt.show()