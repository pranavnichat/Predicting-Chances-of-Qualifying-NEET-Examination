import streamlit as st # type: ignore
import home, account, mock, mock_test_1, mock_test_2, mock_test_3, mock_test_4, mock_test_5, mock_test_6, mock_test_7, mock_test_8, mock_test_9, mock_test_10, prediction

st.set_page_config(
    page_title="NEET Qualifying Portal",
)

class MultiApp:

    def __init__(self):
        self.apps = []
        self.logged_in = False
        self.completed_mock_tests = 0  # Track the number of completed mock tests
        self.total_mock_tests = 10  # Total number of mock tests
        self.available_mock_tests = [mock_test_1, mock_test_2, mock_test_3, mock_test_4, mock_test_5, mock_test_6, mock_test_7, mock_test_8, mock_test_9, mock_test_10]
        self.login_status_checked = False

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def check_login_status(self):
        # Check login status only once
        if not self.login_status_checked:
            # Check if the user is logged in
            if 'username' in st.session_state:
                self.logged_in = True
            self.login_status_checked = True

    def option_menu(self):
        self.check_login_status()  # Check login status
        
        menu_title = 'NEET Qualifying Portal'

        options = ['Home', 'Account', 'Mock', 'Prediction']

        selected_option = st.sidebar.selectbox(menu_title, options)

        # Call the corresponding app function based on the selected option
        if selected_option == 'Home':
            home.app()
        elif selected_option == 'Account':
            account.app()
        elif selected_option == 'Mock':
            # Display mock guideline page
            mock.app()
            # Display subcategories for selecting mock tests from 1 to 10
            selected_mock_test = st.sidebar.selectbox("Select Mock Test", [f"Mock Test {i}" for i in range(1, 11)])
            test_number = int(selected_mock_test.split()[-1])
            self.available_mock_tests[test_number - 1].app()
        elif selected_option == 'Prediction':
            prediction.app()

        # Check if all mock tests are completed and trigger prediction if so
        if self.completed_mock_tests == self.total_mock_tests:
            prediction.app()

multi_app = MultiApp()
multi_app.option_menu()
