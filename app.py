import streamlit as st

def main():
    st.title("Social Media Analyzer")

    # Sidebar with options
    st.sidebar.header("Options")
    social_media_platform = st.sidebar.selectbox("Select social media platform", ["Twitter", "Instagram"])
    username = st.sidebar.text_input("Enter username")

    # Main content
    st.subheader("User Information")
    st.write(f"Selected Social Media Platform: {social_media_platform}")
    st.write(f"Username: {username}")

    # Buttons
    search_button = st.button("Search")
    predict_button = st.button("Predict")

    # Perform actions based on button clicks
    if search_button:
        st.write("Searching...")  # You can replace this with the actual search functionality
    elif predict_button:
        st.write("Predicting...")  # You can replace this with the actual prediction functionality

if __name__ == "__main__":
    main()
