# app/main.py
import streamlit as st
from pages import home, about, question_answer, privacy_policy

def main():
    st.sidebar.title("Navigation")
    pages = {
        "Home": home.show_home_page,
        "About": about.show_about_page,
        "Q&A": question_answer.show_home_page,
        "PrivacyPolicy": privacy_policy.show_home_page,
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selection]()

if __name__ == "__main__":
    main()
