import streamlit as st
import pickle
import requests

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommmender System')
selected_movie_name = st.selectbox('Choose your movie',
                      movies_list)

def fetch_poster(id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NTg0OGY2MjU5YzhmYTkzN2VlMWVhYTI3OTRhNWE0ZSIsInN1YiI6IjY2MzIxMjVhOTlkNWMzMDEyNjU2MTgxMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AKuhtOtstaEEVLQekqwAbAz9YxOJ9C9KVi6ypHjvxyY"
    }
    response = requests.get(url.format(id), headers=headers).json()
    return "https://image.tmdb.org/t/p/w500/"+response['poster_path']


def recommend(str):
    index = movies[movies['title'] == str].index[0]
    distances = similarity[index]
    recommended_movies = []
    recommended_posters = []
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movies.iloc[i[0]].id))
    return recommended_movies , recommended_posters


if st.button('Recommended Movies'):
   names , posters = recommend(selected_movie_name)
   col1, col2, col3, col4, col5 = st.columns(5)
   with col1:
       st.image(posters[0], use_column_width=True)
       st.text(names[0])
   with col2:
       st.image(posters[1], use_column_width=True)
       st.text(names[1])
   with col3:
       st.image(posters[2], use_column_width=True)
       st.text(names[2])
   with col4:
       st.image(posters[3], use_column_width=True)
       st.text(names[3])
   with col5:
       st.image(posters[4], use_column_width=True)
       st.text(names[4])


