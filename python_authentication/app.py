import streamlit as st
import sqlite3
import hashlib

# Function to hash passwords securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a database connection
def get_db_connection():
    conn = sqlite3.connect("users.db")
    return conn

# Function to check if a user exists
def check_user_exists(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to add a new user
def add_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()
    conn.close()

# Function to validate login
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to apply custom styles
def apply_custom_styles():
    st.markdown("""
        <style>
            body {
                background-color: #f8f9fa;
            }
            .stButton>button {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 16px;
                transition: 0.3s;
                border: none;
            }
            .stButton>button:hover {
                background-color: #0056b3;
            }
            .stTextInput>div>div>input {
                border-radius: 5px;
                padding: 8px;
                border: 1px solid #ced4da;
            }
            h2 {
                color: #333;
            }
        </style>
    """, unsafe_allow_html=True)

# Streamlit UI
def main():
    apply_custom_styles()  # Apply styles

    st.title("User Authentication System")

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if login_user(username, password):
                st.success(f"Welcome, {username}!")
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
            else:
                st.error("Invalid Username or Password!")

    elif choice == "Sign Up":
        st.subheader("Sign Up")
        new_username = st.text_input("Username", key="signup_user")
        new_password = st.text_input("Password", type="password", key="signup_pass")

        if st.button("Sign Up"):
            if check_user_exists(new_username):
                st.error("Username already exists! Try another.")
            else:
                add_user(new_username, new_password)
                st.success("Account created successfully! You can now log in.")

    # Logout Button
    if st.session_state.get("logged_in", False):
        if st.button("Logout", key="logout_button"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.success("You have logged out.")

if __name__ == "__main__":
    main()
