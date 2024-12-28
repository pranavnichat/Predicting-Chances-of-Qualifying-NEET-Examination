import streamlit as st  # type: ignore
import pyodbc # type: ignore

# Database connection configuration
server = 'PALLAVINAKE2304\SQLEXPRESS'  # Assuming SQL Server is running locally
database = 'NeetRegistration'

# Function to connect to the database
def connect_to_database():
    try:
        conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database}')
        cursor = conn.cursor()
        return conn, cursor
    except pyodbc.Error as e:
        st.error(f"Failed to connect to SQL Server: {e}")
        return None, None

# Function to fetch data from the database
def fetch_data(table_name):
    conn, cursor = connect_to_database()
    if conn and cursor:
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            conn.close()
            return data
        except pyodbc.Error as e:
            st.error(f"Failed to fetch data from the database: {e}")
            return None
    else:
        return None

# Streamlit app
def main():
    st.title('Admin Panel')

    # Fetch data from a selected table
    selected_table = st.selectbox('Select Users', ['Users', 'Results'])
    data = fetch_data(selected_table)

    # Display the fetched data
    if data:
        st.write(f"Showing data from the {selected_table} table:")
        st.write(data)
    else:
        st.warning("Failed to fetch data from the database.")

if __name__ == '__main__':
    main()
