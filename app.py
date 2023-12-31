import streamlit as st
import instaloader
import numpy as np
import pickle
import requests
from sklearn.ensemble import RandomForestClassifier

# URLs for the pickled model and scaler
sc_url = 'https://github.com/Dineshjnld/frontend-fake-detect/raw/main/scaler.pkl'
rfc_url = 'https://github.com/Dineshjnld/frontend-fake-detect/raw/main/rfc.pkl'

# Fetch StandardScaler
with requests.get(sc_url, stream=True) as sc_file:
    sc = pickle.load(sc_file.raw)

# Fetch RandomForestClassifier
with requests.get(rfc_url, stream=True) as rfc_file:
    rfc = pickle.load(rfc_file.raw)

def fetch_instagram_details(username):
    # Create an Instaloader instance
    ig = instaloader.Instaloader()

    # Fetch profile information
    profile = instaloader.Profile.from_username(ig.context, username)

    # Display fetched details
    st.write("Username:", profile.username)
    st.write("Number of digits in username:", sum(char.isdigit() for char in profile.username))
    st.write("Number of words in username:", len(profile.username.split()))
    st.write("Number of digits in full name:", sum(char.isdigit() for char in profile.full_name))
    st.write("Number of words in full name:", len(profile.full_name.split()))
    st.write("Full Name:", profile.full_name)
    st.write("Number of Posts Uploads:", profile.mediacount)
    st.write("Bio:", profile.biography)

    if profile.external_url:
        st.write("External URL:", profile.external_url)
    else:
        st.write("No External URL set.")

    if profile.is_private:
        st.write("Account is private.")
    else:
        st.write("Account is not private.")

    return profile

def predict_spam(profile_data):
    global sc, rfc
    # Convert the user input to a NumPy array
    user_input = np.array([[
        profile_data['profile_pic'], profile_data['num_by_num'], profile_data['full_name'],
        profile_data['num_by_char'], profile_data['name_username'], profile_data['bio_len'],
        profile_data['url'], profile_data['private'], profile_data['post'],
        profile_data['followers'], profile_data['follows']
    ]])

    # Standardize the user input using the same scaler used during training
    user_input_scaled = sc.transform(user_input)

    # Make predictions for the user input
    prediction = rfc.predict(user_input_scaled)
    prob = rfc.predict_proba(user_input_scaled)

    # Display the prediction result
    st.write("Prediction:")
    if prediction == 0:
        st.write('0: Genuine account')
    else:
        st.write('1: Spam account')

    prob_percentage = prob[:, prediction] * 100
    percentage_value = prob_percentage.item()
    st.write('Probability : {:.0f}%'.format(percentage_value))

def main():
    st.title("Account Analyzer")

    # Select social media platform
    social_media_platform = st.selectbox("Select social media platform", ["Twitter", "Instagram"])

    # Input box for username
    username = st.text_input("Enter username")

    # Button to fetch Instagram details
    if st.button("Search"):
        if social_media_platform == "Instagram":
            profile_data = fetch_instagram_details(username)

    # Button to predict
    if st.button("Predict"):
        if social_media_platform == "Instagram":
            if profile_data:
                predict_spam(profile_data)

if __name__ == "__main__":
    main()
