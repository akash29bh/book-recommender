import streamlit as st
import pickle
import numpy as np

# Load the pre-trained models and data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


# Streamlit app structure
def main():
    st.title("Book Recommendation System")

    # Sidebar navigation
    navigation = st.sidebar.radio("Navigation", ["Home", "Recommend"])

    if navigation == "Home":
        show_home_page()
    elif navigation == "Recommend":
        show_recommendation_page()


def show_home_page():
    st.header("Popular Books")
    # Display popular books
    for index, row in popular_df.iterrows():
        st.image(row['Image-URL-M'], width=100)
        st.write(f"**{row['Book-Title']}** by {row['Book-Author']}")
        st.write(f"Rating: {row['avg_rating']} ({row['num_ratings']} ratings)")
        st.write("---")


def show_recommendation_page():
    st.header("Book Recommendations")
    user_input = st.text_input("Enter a book title:")

    if st.button("Recommend Books"):
        if user_input:
            recommend_books(user_input)
        else:
            st.error("Please enter a book title.")


def recommend_books(user_input):
    try:
        # Find the index of the book
        index = np.where(pt.index == user_input)[0][0]
        # Get similar items based on the similarity scores
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)

        # Display recommended books
        st.write("Recommended Books:")
        for item in data:
            st.image(item[2], width=100)
            st.write(f"**{item[0]}** by {item[1]}")
            st.write("---")
    except IndexError:
        st.error("Book not found. Please try another title.")


if __name__ == '__main__':
    main()