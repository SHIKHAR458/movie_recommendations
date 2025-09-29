import streamlit as st
import joblib
import difflib

movies = joblib.load("movies.joblib")
similarity = joblib.load("similarity.joblib")


def recommend(movie):
    """Recommends 5 movies based on content similarity."""
    list_of_all_titles = movies['title'].tolist()

    try:
        close_match = difflib.get_close_matches(movie, list_of_all_titles, n=1, cutoff=0.6)[0]
    except IndexError:
        return []

    movie_index = movies[movies['title'] == close_match].index[0]

    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_names = []
    for i in movies_list:
        recommended_movies_names.append(movies.iloc[i[0]].title)

    return recommended_movies_names

st.set_page_config(layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #001f3f; 
    color: #ffffff;     
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #003366; 
    color: #ffffff;
}

.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 24px;
    font-size: 16px;
    transition: background-color 0.3s ease;
}
.stButton>button:hover {
    background-color: #ff6a6a; 
    color: white;
}

h1, h3 {
    color: #ff4b4b; 
    text-align: center;
}

.stSuccess {
    background-color: rgba(0, 51, 102, 0.6); 
    border-radius: 8px;
    text-align: center;
    padding: 10px;
}

.netflix-logo-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px; 
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="netflix-logo-container">', unsafe_allow_html=True)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netflix_2015_logo.svg/langfr-1920px-Netflix_2015_logo.svg.png", width=200) # You can adjust the width
st.markdown('</div>', unsafe_allow_html=True)

st.title("🎬 Movie Recommendation System")

movie_list = movies['title'].values
options = ["--Select a movie--"] + list(movie_list)

selected_movie = st.selectbox(
    "Type or select a movie to get recommendations:",
    options 
)

if st.button("Show Recommendations"):
    if selected_movie != "--Select a movie--":
        with st.spinner('Finding similar movies for you...'):
            recommended_movie_names = recommend(selected_movie)

            if recommended_movie_names:
                st.write("---") 
                st.header("Here are some movies you might like:")

                cols = st.columns(5, gap="medium")
                for i in range(len(recommended_movie_names)):
                    with cols[i]:
                        st.success(recommended_movie_names[i])
            else:
                 st.warning("Could not find recommendations for that movie. Please try another.")
    else:
        st.warning("Please select a movie from the dropdown first.")