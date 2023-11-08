import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

def load_data():
    netflix = pd.read_csv('netflix.csv')
    for column in netflix:
        netflix[column] = netflix[column].fillna('')
    return netflix

def preprocess_data(netflix):
    combine_columns = netflix['director'] + ' ' + netflix['cast'] + ' ' + netflix['listed_in'] + ' ' + netflix['description']
    vectorizer = TfidfVectorizer()
    feature_vector = vectorizer.fit_transform(combine_columns)
    similarity = cosine_similarity(feature_vector)
    return similarity, netflix

netflix = load_data()
similarity, netflix = preprocess_data(netflix)

st.title("Netflix Movie Recommendation System")

movie_name = st.text_input("Enter a movie name:")

if movie_name:
    title_list = netflix['title'].tolist()
    find_match = difflib.get_close_matches(movie_name, title_list)

    if not find_match:
        st.write("Movie not found.")
    else:
        close_match = find_match[0]
        movie_index = netflix[netflix['title'] == close_match].index.values

        if len (movie_index) == 0:
            st.write("Movie not found.")
        else:
            movie_index = movie_index[0]
            similarity_score = list(enumerate(similarity[movie_index]))
            sort_movie = sorted(similarity_score, key=lambda x: x[1], reverse=True)

            st.write(f"Recommended movies similar to '{close_match}':")
            for i, movie in enumerate(sort_movie):
                index = movie[0]
                title_from_index = netflix.loc[index, 'title']
                if i < 20:
                    st.write(f"{i + 1}. {title_from_index}")

