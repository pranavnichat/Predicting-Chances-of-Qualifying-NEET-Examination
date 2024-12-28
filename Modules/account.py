import streamlit as st # type: ignore
import pyodbc # type: ignore
import re
import random
import string
from datetime import datetime, timedelta

# Database connection configuration
server = 'PALLAVINAKE2304\SQLEXPRESS'  # Assuming SQL Server is running locally
database = 'NeetRegistration'

# Connect to SQL Server
try:
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database}')
    cursor = conn.cursor()
except pyodbc.Error as e:
    st.error(f"Failed to connect to SQL Server: {e}")
    st.stop()

# Email validation function
def is_valid_email(email):
    email_regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    return re.match(email_regex, email) is not None

# Password strength validation function
def is_strong_password(password):
    min_length = 8
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in password)
    
    return (
        len(password) >= min_length and
        has_uppercase and
        has_lowercase and
        has_digit and
        has_special
    )

# Unique ID generation function
def generate_unique_id():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(8))

# Mobile number validation function
def is_valid_mobile(mobile):
    return re.match(r'^\d{10}$', mobile) is not None

# Signup with email, password, username, category, mobile number, and date of birth
def sign_up_with_email_and_password(name, email, mobile, unique_id, password, confirm_password, dob, category):
    try:
        if password != confirm_password:
            st.warning("Passwords do not match!")
            return

        # Check if age is at least 15 years
        min_date = datetime.today() - timedelta(days=15*365)  # 15 years ago
        if dob > min_date.date():
            st.warning("You must be at least 15 years old to register.")
            return

        # Save user data to the database
        cursor.execute("INSERT INTO Users (UniqueID, FullName, Email, MobileNo, Passwords, DoB, Category) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (unique_id, name, email, mobile, password, dob.strftime('%Y-%m-%d'), category))
        conn.commit()

        # Return success message
        st.success("Registration successful!")
    except Exception as e:
        st.warning(f'Signup failed: {e}')


# User registration UI
def user_registration():
    st.title('User Registration')
    name = st.text_input('Name', key='user_name')
    email = st.text_input('Email Address', key='user_email')
    mobile = st.text_input('Mobile Number', key='user_mobile')
    unique_id = st.text_input('Unique ID', key='user_unique_id')
    password = st.text_input('Password', type='password', key='user_password')
    confirm_password = st.text_input('Confirm Password', type='password', key='user_confirm_password')
    
    # Set the range of dates to display the whole year
    max_date = datetime(datetime.today().year, 12, 31).date()
    min_date = datetime(datetime.today().year - 100, 1, 1).date()

    dob = st.date_input('Date of Birth', min_value=min_date, max_value=max_date, key='user_dob')
    
    st.write(f"You must be at least 15 years old to register.")

    category_options = ['GEN', 'OBC', 'SC', 'ST', 'NT', 'EWS']
    category = st.selectbox('Category', category_options, key='user_category')
    
    if st.button('Register'):
        unique_id = generate_unique_id()
        sign_up_with_email_and_password(name, email, mobile, unique_id, password, confirm_password, dob, category)

# User login function
def user_login():
    st.title("User Login")
    
    email = st.text_input('Email', key='user_login_email')
    password = st.text_input('Password', type='password', key='user_login_password')

    # Create a login button
    if st.button('Login', key='user_login_button'):
        try:
            # Query the Users table to check if the provided email and password are valid
            cursor.execute("SELECT * FROM Users WHERE Email = ?", (email,))
            user = cursor.fetchone()

            # Check if user exists and set the username in session state
            if user:
                if user.Passwords == password:  # Assuming 'Passwords' is the column name for password
                    st.write("Login successful!")
                    st.session_state.loggedin = True
                    st.session_state.username = user.FullName  # Assuming 'FullName' is the column name for username
                    st.success("Login successful! Welcome.")
                    return True
                else:
                    st.write("Invalid email or password.")
                    return False
            else:
                st.write("User not found.")
                return False
                
        except pyodbc.Error as e:
            # Error occurred during SQL query execution
            st.error(f"An error occurred while executing the SQL query: {e}")
            return False

# Admin login function
def admin_login(username, password):
    try:
        # Query the Admins table to check if the provided username and password are valid
        cursor.execute("SELECT * FROM Admins WHERE Username = ? AND Passwords = ?", (username, password))
        admin = cursor.fetchone()

        # Check if admin exists and set the admin_loggedin status
        if admin:
            st.session_state.admin_loggedin = True
            st.success("Admin loggedin successfully!")

        
        else:
            st.error("Invalid username or password.")
            return False
                
    except pyodbc.Error as e:
        # Error occurred during SQL query execution
        st.error(f"An error occurred while executing the SQL query: {e}")
        return False

# Admin logout function
def admin_logout():
    st.session_state.pop('admin_loggedin', None)
    st.success("Admin logged out successfully!")

# Admin login UI
def admin_login_page():
    st.title("Admin Login")
    
    username = st.text_input('Username', key='admin_username')
    password = st.text_input('Password', type='password', key='admin_password')

    # Create a login button
    if st.button('Login as Admin', key='admin_login_button'):
        admin_login(username, password)

# Main app function
def app():
    st.title('Welcome to Chances of Qualifying NEET Examination Portal')
    
    # Initialize session state variables
    st.session_state.setdefault('loggedin', False)  # Track user login status
    st.session_state.setdefault('admin_loggedin', False)  # Track admin login status
    
    # Check if the admin is logged in
    if st.session_state.admin_loggedin:
        st.title("Admin Dashboard")
        if st.button('Logout as Admin'):
            admin_logout()  # Call the admin logout function
    else:
        # Check if the user is logged in
        if not st.session_state.loggedin:
            choice = st.selectbox('Login', ['User', 'Admin'])

            if choice == 'User':
                user_registration()  # Call the user registration function or
                user_login() # Call the user login function
            elif choice == 'Admin':
                admin_login_page()  # Call the admin login page function
                    
        else:
            st.title("You're Logged In")
            st.write(f"Welcome, {st.session_state.username}!")  # Assuming you'll retrieve and store the username after login

            # Add logout button
            if st.button('Log out'):
                st.session_state.loggedin = False
                st.success("Logged out successfully!")
    
if __name__ == "__main__":
    app()
