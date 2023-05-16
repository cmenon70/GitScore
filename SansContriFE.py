import streamlit as st
import pandas as pd
import SansContri as cp

# Function to fetch user details from GitHub based on the username

def main():
    st.title("Github Scoring")

    # show both options to the user
    st.write("Choose an option:")
    csv_file = st.file_uploader("Upload CSV", type=["csv"])
    st.markdown('<div style="text-align: center;">-- OR --</div>', unsafe_allow_html=True)
    github_username = st.text_input("Enter GitHub Username")

    # check which option the user chose
    if csv_file is not None:
        # user uploaded a CSV file, perform data analysis on it
        cp.getuserdeetswithCSV(csv_file)
        # your data analysis code goes here
    elif github_username != "":
        # user entered a GitHub username, fetch user details and display them
        st.write("GitHub User Details:")
        user_details = cp.getuserdeets(github_username)
        # your code to display user details goes here
    else:
        # no option selected yet
        st.write("Please select an option")

if __name__ == "__main__":
    main()