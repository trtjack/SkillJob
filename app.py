import streamlit as st
import requests
import bcrypt

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""


def login_page():
    with st.container():
        st.title("Welcome")

        with st.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Log In")

            if submit_button:
                github_url = "https://raw.githubusercontent.com/Bogdan8769/SkillJob/refs/heads/main/login_details_app.json"

                try:
                    response = requests.get(github_url)
                    response.raise_for_status()
                    user_database = response.json()

                    if email in user_database:
                        stored_hash = user_database[email]["hash"].encode('utf-8')
                        password_bytes = password.encode('utf-8')

                        if bcrypt.checkpw(password_bytes, stored_hash):
                            st.session_state.logged_in = True
                            st.session_state.user_name = user_database[email]["name"]
                            st.rerun()
                        else:
                            st.error("Incorrect password.")
                    else:
                        st.error("Email not found.")

                except Exception as e:
                    st.error(f"Could not connect to the database. Error: {e}")


def main_page():
    col1, col2 = st.columns([8, 2])

    with col1:
        st.title("Main Dashboard")
        st.write("You are securely logged in. Let's build the app here.")

    with col2:
        st.write("\n")
        st.write(f"👤 **{st.session_state.user_name}**")

        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.rerun()



if st.session_state.logged_in:
    main_page()
else:
    login_page()
