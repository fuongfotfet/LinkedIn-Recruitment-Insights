from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import re

df_vn = pd.read_csv('linkedin-job-Vietnam-cut.csv')
df_us = pd.read_csv('linkedin-job-US-cut.csv')
df_vcb = pd.read_csv('VCB-job-Vietnam.csv')

# Define a function to create word clouds from titles
def create_word_cloud(df, title_column):
    # Combine all titles into one large text string
    text = " ".join(title for title in df[title_column])
    # Generate a word cloud image
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    # Display the generated image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# Create word clouds for each dataset
create_word_cloud(df_vn, "title")
create_word_cloud(df_us, "title")
create_word_cloud(df_vcb, "title")

# Define a function to create word clouds from descriptions, removing all HTML tags, entities, and special characters
def create_word_cloud_fully_cleaned_description(df, description_column):
    # Combine all descriptions into one large text string, removing all HTML tags, entities, and special characters
    text = " ".join(re.sub(r'<[^>]+>|&[a-z]+;|&#[0-9]+;', ' ', desc) for desc in df[description_column].dropna())
    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)
    # Generate a word cloud image
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    # Display the generated image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# Create word clouds for fully cleaned descriptions in each dataset
create_word_cloud_fully_cleaned_description(df_vn, "description")
create_word_cloud_fully_cleaned_description(df_us, "description")
create_word_cloud_fully_cleaned_description(df_vcb, "description")