import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.metrics import mean_squared_error

df = pd.read_csv('./ratings_Electronics (1).csv', header=None)

# Adding column names
df.columns = ['user_id', 'prod_id', 'rating', 'timestamp']

# Dropping timestamp column
df = df.drop('timestamp', axis=1)

# Copying the data to another dataframe
df_copy = df.copy(deep=True)

# Get the number of rows and columns
rows, columns = df.shape[0], df.shape[1]
print("No of rows: ", rows)
print("No of columns: ", columns)

# Check for missing values
df.isna().sum()

# Summary statistics of 'rating' variable
df.describe()

# Top 10 users based on rating
most_rated = df.groupby('user_id').size().sort_values(ascending=False)[:10]
most_rated

# Count the number of ratings per user and filter users with at least 50 ratings
counts = df['user_id'].value_counts()
df_final = df[df['user_id'].isin(counts[counts >= 50].index)]
print('The number of observations in the final data =', len(df_final))
print('Number of unique USERS in the final data = ', df_final['user_id'].nunique())
print('Number of unique PRODUCTS in the final data = ', df_final['prod_id'].nunique())

# Create the interaction matrix of products and users based on ratings and replace NaN value with 0
final_ratings_matrix = df_final.pivot(index='user_id', columns='prod_id', values='rating').fillna(0)
print('Shape of final_ratings_matrix: ', final_ratings_matrix.shape)

# Finding the number of non-zero entries in the interaction matrix
given_num_of_ratings = np.count_nonzero(final_ratings_matrix)
print('given_num_of_ratings = ', given_num_of_ratings)

# Finding the possible number of ratings as per the number of users and products
possible_num_of_ratings = final_ratings_matrix.shape[0] * final_ratings_matrix.shape[1]
print('possible_num_of_ratings = ', possible_num_of_ratings)

# Density of ratings
density = (given_num_of_ratings / possible_num_of_ratings)
density *= 100
print('density: {:4.2f}%'.format(density))

final_ratings_matrix.head()

final_ratings_matrix['user_index'] = np.arange(0, final_ratings_matrix.shape[0])
final_ratings_matrix.set_index(['user_index'], inplace=True)

# Actual ratings given by users
final_ratings_matrix.head()

# Define a function to get similar users
def similar_users(user_index, interactions_matrix):
    similarity = []
    for user in range(0, interactions_matrix.shape[0]):
        # Finding cosine similarity between the user_id and each user
        sim = cosine_similarity([interactions_matrix.loc[user_index]], [interactions_matrix.loc[user]])
        # Appending the user and the corresponding similarity score with user_id as a tuple
        similarity.append((user, sim))

    similarity.sort(key=lambda x: x[1], reverse=True)
    most_similar_users = [Tuple[0] for Tuple in similarity]  # Extract the user from each tuple in the sorted list
    similarity_score = [Tuple[1] for Tuple in similarity]  # Extract the similarity score from each tuple in the sorted list

    # Remove the original user and its similarity score and keep only other similar users
    most_similar_users.remove(user_index)
    similarity_score.remove(similarity_score[0])

    return most_similar_users, similarity_score

similar = similar_users(5, final_ratings_matrix)[0][0:10]

# Print the similarity score
print(similar_users(5, final_ratings_matrix)[1][0:10])

similar = similar_users(1521, final_ratings_matrix)[0][0:10]
similar

# Print the similarity score
print(similar_users(1521, final_ratings_matrix)[1][0:10])

# Define the recommendations function to get recommendations using the similar users' preferences
def recommendations(user_index, num_of_products, interactions_matrix):
    # Saving similar users using the function similar_users defined above
    most_similar_users = similar_users(user_index, interactions_matrix)[0]

    # Finding product IDs with which the user_id has interacted
    prod_ids = set(list(interactions_matrix.columns[np.where(interactions_matrix.loc[user_index] > 0)]))
    recommendations = []

    observed_interactions = prod_ids.copy()
    for similar_user in most_similar_users:
        if len(recommendations) < num_of_products:
            # Finding 'n' products which have been rated by similar users but not by the user_id
            similar_user_prod_ids = set(
                list(interactions_matrix.columns[np.where(interactions_matrix.loc[similar_user] > 0)]))
            recommendations.extend(list(similar_user_prod_ids.difference(observed_interactions)))
            observed_interactions = observed_interactions.union(similar_user_prod_ids)
        else:
            break
    print(recommendations[:num_of_products])
    return recommendations[:num_of_products]

recommendations(8, 5, final_ratings_matrix)
