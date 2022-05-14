import streamlit as st
import sqlite3
import pandas as pd

#DB management
conn = sqlite3.connect('data.db')
c = conn.cursor()


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT UNIQUE, password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username=? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():

    st.title("Simple Login App")

    menu = ["Home", "Login", "SignUp"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.sidebar.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.checkbox("Login"):
            # if password == "12345":
            create_usertable()
            if login_user(username, password):
                st.sidebar.success("Logged In as {}".format(username))

                task = st.selectbox("Task", ["Add Post", "Analytics", "Profiles"])
                if task == "Add Post":
                    st.subheader("Add Post")
                elif task == "Analytics":
                    st.subheader("Analytics")
                elif task == "Profiles":
                    st.subheader("Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
                    st.dataframe(clean_db)
            else:
                st.sidebar.error("Incorrect Username/Password!")

    elif choice == "SignUp":
        st.sidebar.subheader("Create New Account")
        new_user = st.sidebar.text_input("Username")
        new_password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.button("Signup"):
            if new_user == "" and new_password == "":
                st.sidebar.error("Please insert username and password!")
            elif new_user == "":
                st.sidebar.error("Please insert username!")
            elif new_password == "":
                st.sidebar.error("Please insert password!")
            else:
                create_usertable()
                try:
                    add_userdata(new_user, new_password)
                    st.sidebar.success("You have succesfully created a valid account!")
                    st.sidebar.info("Go to Login Menu to login!")
                except:
                    st.sidebar.error("Username already exists! Insert a new one!")


if __name__ == '__main__':
    main()