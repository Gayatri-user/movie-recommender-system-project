
import streamlit as st
import pickle
import requests

# ----------------------------
# Secure API Key
# ----------------------------
api_key = st.secrets["OMDB_API_KEY"]

# ----------------------------
# Load Data
# ----------------------------
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ----------------------------
# Fetch Movie Details
# ----------------------------
def fetch_movie_details(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    poster = data.get("Poster")
    plot = data.get("Plot")

    if poster == "N/A" or poster is None:
        poster = None

    if plot == "N/A" or plot is None:
        plot = "No description available."

    return poster, plot


# ----------------------------
# Recommendation Function
# ----------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []
    plots = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        poster, plot = fetch_movie_details(title)

        names.append(title)
        posters.append(poster)
        plots.append(plot)

    return names, posters, plots


# ----------------------------
# UI
# ----------------------------
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Choose a movie",
    movies['title'].values
)

if st.button("Recommend"):

    st.subheader("🎥 Selected Movie")

    selected_poster, selected_plot = fetch_movie_details(selected_movie)

    col1, col2 = st.columns([1, 2])

    with col1:
        if selected_poster:
            st.image(selected_poster, use_container_width=True)
        else:
            st.write("No Poster Available")

    with col2:
        st.markdown(f"### {selected_movie}")
        st.write(selected_plot)

    st.subheader("🍿 Recommended Movies")

    names, posters, plots = recommend(selected_movie)

    cols = st.columns(5)

    for col, name, poster, plot in zip(cols, names, posters, plots):
        with col:
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.write("No Poster Available")

            st.markdown(f"**{name}**")
            st.caption(plot[:120] + "...")

