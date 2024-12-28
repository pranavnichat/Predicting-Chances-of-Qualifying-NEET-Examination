import streamlit as st # type: ignore
import pandas as pd
import pyodbc # type: ignore
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Database connection configuration
server = 'PALLAVINAKE2304\SQLEXPRESS'
database = 'NeetRegistration'

# Connect to SQL Server
try:
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database}')
    cursor = conn.cursor()
except pyodbc.Error as e:
    st.error(f"Failed to connect to SQL Server: {e}")
    st.stop()

# Function to fetch user data from the database based on unique ID
def fetch_user_data(unique_id):
    try:
        cursor.execute("SELECT Category FROM Users WHERE UniqueID = ?", (unique_id,))
        user_data = cursor.fetchone()
        if user_data:
            return user_data[0]
        else:
            st.warning("No user data found for the current user.")
            return None
    except pyodbc.Error as e:
        st.error(f"An error occurred while fetching user data: {e}")
        return None

# Function to fetch mock test results from the database based on unique ID
def fetch_mock_test_results(unique_id):
    try:
        cursor.execute("SELECT mocktest1, mocktest2, mocktest3, mocktest4, mocktest5, mocktest6, mocktest7, mocktest8, mocktest9, mocktest10 FROM Results WHERE UniqueID = ?", (unique_id,))
        mock_test_results = cursor.fetchone()
        if mock_test_results:
            return mock_test_results
        else:
            st.warning("No mock test results found for the current user.")
            return None
    except pyodbc.Error as e:
        st.error(f"An error occurred while fetching mock test results: {e}")
        return None

# Preprocess data
def preprocess_data(user_data, mock_test_results):
    if user_data is None or mock_test_results is None:
        return None

    df = pd.DataFrame([mock_test_results], columns=['mocktest1', 'mocktest2', 'mocktest3', 'mocktest4', 'mocktest5', 'mocktest6', 'mocktest7', 'mocktest8', 'mocktest9', 'mocktest10'])
    df['Category'] = user_data
    return df

# Train model
def train_model(df):
    if df is None:
        return None

    X = df.drop(columns=['Category'])
    y = df['Category']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model

# Define determine_qualification function
def determine_qualification(predicted_score, category):
    if category in ["GEN", "OBC"]:
        if 600 <= predicted_score <= 720:
            return "High Chance of Qualification"
        elif 400 <= predicted_score < 600:
            return "Moderate Chance of Qualification"
        else:
            return "Unlikely to Qualify"
    elif category == "SC":
        if predicted_score >= 250:
            return "Moderate Chance of Qualification"
        else:
            return "Unlikely to Qualify"
    elif category == "ST":
        if predicted_score >= 300:
            return "Moderate Chance of Qualification"
        else:
            return "Unlikely to Qualify"
    elif category == "EWS":
        if 550 <= predicted_score <= 720:
            return "High Chance of Qualification"
        elif 350 <= predicted_score < 550:
            return "Moderate Chance of Qualification"
        else:
            return "Unlikely to Qualify"
    else:
        return "Invalid Category"

# Streamlit app
def app():
    st.title("NEET Qualification Predictor")

    # Check if user is logged in
    if 'unique_id' not in st.session_state or not st.session_state['unique_id']:
        st.error('Please login first.')
        return

    # Fetch user data from the database based on the session's unique ID
    user_data = fetch_user_data(st.session_state['unique_id'])

    # Fetch mock test results from the database based on the session's unique ID
    mock_test_results = fetch_mock_test_results(st.session_state['unique_id'])

    # Preprocess data
    df = preprocess_data(user_data, mock_test_results)

    # Train model
    model = train_model(df)

    # Button to predict the final score
    if st.button("Predict the final score"):
        if model is None:
            st.error("Model is not trained. Cannot make predictions.")
        else:
            # Predict the NEET Final Score using the trained model
            prediction = model.predict(df.drop(columns=['Category']))
            st.write("Predicted NEET Final Score:", prediction[0])

            # Determine qualification based on predicted score and user category
            qualification = determine_qualification(prediction[0], user_data)
            st.write("Qualification Prediction:", qualification)

            st.success("Best of Luck for Your Exam!")

if __name__ == "__main__":
    app()
