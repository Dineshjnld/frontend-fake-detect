import streamlit as st
import instaloader
import numpy as np
import joblib
# Load your machine learning model and StandardScaler
# Assuming 'sc' is the StandardScaler used during training
# Assuming 'rfc' is the trained Random Forest Classifier
# Load them as per your actual model loading process

# Placeholder for the machine learning model and StandardScaler
sc = joblib.load('scaler1.joblib')
rfc = joblib.load('rfc1.joblib')

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
    st.title(" Account Analyzer")

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
