import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

data = {
    'user_id': [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5],
    'movie_id': [101, 102, 103, 101, 104, 102, 103, 105, 101, 103, 102, 104],
    'rating': [5, 4, 3, 4, 5, 4, 5, 2, 3, 5, 4, 5]
}

df = pd.DataFrame(data)

user_item_matrix = df.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)

user_similarity = cosine_similarity(user_item_matrix)

user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

def get_similar_users(user_id, top_n=2):
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)
    similar_users = similar_users.drop(user_id)  
    return similar_users.head(top_n)

def recommend_movies(user_id, top_n=2):
    similar_users = get_similar_users(user_id, top_n=top_n)
    
    similar_users_ratings = user_item_matrix.loc[similar_users.index]
    
    movie_recommendations = similar_users_ratings.sum().sort_values(ascending=False)
    
    user_rated_movies = user_item_matrix.loc[user_id]
    movie_recommendations = movie_recommendations.drop(user_rated_movies[user_rated_movies > 0].index, errors='ignore')
    
    return movie_recommendations.head()

recommended_movies = recommend_movies(user_id=1, top_n=2)
print("Recommended Movies for User 1:")
print(recommended_movies)
