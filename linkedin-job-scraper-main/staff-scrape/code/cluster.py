import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
boa_it_df = pd.read_csv('BOA_IT.csv')
deloitte_it_df = pd.read_csv('Deloitte_IT.csv')

# Extract the 'current_position' columns from both datasets
boa_current_position = boa_it_df[['current_position']]
deloitte_current_position = deloitte_it_df[['current_position']]

# Combine both current_position columns into a single dataframe
combined_positions = pd.concat([boa_current_position, deloitte_current_position], ignore_index=True)

# Let's perform a simple string vectorization to convert these positions into a numerical form
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
# Use TF-IDF vectorizer to transform the job titles into a numerical matrix
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(combined_positions['current_position'].fillna(''))

# Apply DBSCAN clustering
dbscan = DBSCAN(eps=0.3, min_samples=5, metric='cosine')
clusters = dbscan.fit_predict(X)

# Add the cluster labels back to the dataframe
combined_positions['cluster'] = clusters

plt.figure(figsize=(8, 6))
sns.countplot(x='cluster', data=combined_positions)
plt.title('Distribution of Best Clusters for Current Positions')
plt.xlabel('Cluster')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.savefig('cluster.png')
plt.show()

valid_best_clusters = combined_positions['cluster'] != -1

# Calculate the silhouette score only for the valid clusters
silhouette_best_score = silhouette_score(X[valid_best_clusters], combined_positions['cluster'][valid_best_clusters], metric='cosine')

print(silhouette_best_score)

roles_by_cluster = combined_positions.groupby('cluster')['current_position'].apply(list)

roles_by_cluster.to_excel('cluster.xlsx',index = False)