import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ac55818b4a81334db327a718cb5392fe&language=en-US'.format(movie_id))
    data = response.json()
    st.text(data)
    st.text('https://api.themoviedb.org/3/movie/{}?api_key=ac55818b4a81334db327a718cb5392fe&language=en-US'.format(movie_id))
    return "https://image.tmdb.org/t/p/w185/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movie_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_list['title'].values
st.title('Movie-Recommender System')

Selected_movie_name = st.selectbox(
    'may you find your suitable genere!!!',
    movies['title'].values)



if st.button(' Recommended'):
    names, posters = recommend(Selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

