from streamlit_option_menu import option_menu
import os
import pickle
import streamlit as st
import re  # Regular expression for email validation
import pandas as pd  # For displaying the table

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Get the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Paths to the saved models
diabetes_model_path = os.path.join(working_dir, 'saved_models', 'diabetes_model.sav')
heart_disease_model_path = os.path.join(working_dir, 'saved_models', 'heart_disease_model.sav')
parkinsons_model_path = os.path.join(working_dir, 'saved_models', 'parkinsons_model.sav')

# Load the models with error handling
try:
    diabetes_model = pickle.load(open(diabetes_model_path, 'rb'))
    heart_disease_model = pickle.load(open(heart_disease_model_path, 'rb'))
    parkinsons_model = pickle.load(open(parkinsons_model_path, 'rb'))
except FileNotFoundError as e:
    st.error(f"Error loading model: {e}. Ensure all models are in the 'saved_models' directory.")
    st.stop()  # Stop further execution

# Function to check if all inputs are filled
def check_empty_inputs(inputs):
    return any(x == "" for x in inputs)

# Function to validate email
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# User registration (For demo purpose, we'll store these in session_state, but in production, it should be a secure database)
if "users" not in st.session_state:
    st.session_state.users = {}

# Login Page
def login_page():
    st.title("Login")

    name = st.text_input("Full Name")
    email = st.text_input("Email (Gmail)")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        # Validate inputs
        if not name:
            st.error("Please enter your name.")
        elif not email or not is_valid_email(email):
            st.error("Please enter a valid Gmail address.")
        elif not password or len(password) < 8:
            st.error("Password must be at least 8 characters long.")
        else:
            # Check if the email is already registered
            if email in st.session_state.users:
                stored_name, stored_password = st.session_state.users[email]
                if stored_password == password:
                    st.session_state.logged_in = True
                    st.session_state.user_name = name  # Store user name for later use
                    st.success("Login successful! Redirecting to the main page...")
                else:
                    st.error("Incorrect password. Please try again.")
            else:
                st.error("Email not registered. Please sign up first.")

# Sign up Page (Allow users to create an account)
def signup_page():
    st.title("Sign Up")

    name = st.text_input("Full Name")
    email = st.text_input("Email (Gmail)")
    password = st.text_input("Password", type='password')

    if st.button("Sign Up"):
        # Validate inputs
        if not name:
            st.error("Please enter your name.")
        elif not email or not is_valid_email(email):
            st.error("Please enter a valid Gmail address.")
        elif not password or len(password) < 8:
            st.error("Password must be at least 8 characters long.")
        else:
            # Check if the email is already taken
            if email not in st.session_state.users:
                st.session_state.users[email] = (name, password)
                st.success("Sign Up successful! You can now log in.")
            else:
                st.error("Email is already registered.")

# Check if the user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    # Option for Login or Sign Up
    option = st.selectbox("Select an option", ("Login", "Sign Up"))

    if option == "Login":
        login_page()  # Show login page if not logged in
    else:
        signup_page()  # Show sign-up page if the user selects Sign Up
else:
    
    # Sidebar for the welcome message above the navigation options
    with st.sidebar:
        st.markdown(f"<h2 style='font-size: 30px; font-weight: bold;'>Welcome, {st.session_state.user_name}!</h2>", unsafe_allow_html=True)
        selected = option_menu('Multiple Disease Prediction System',
                               ['Diabetes Prediction',
                                'Heart Disease Prediction',
                                'Parkinsons Prediction',
                                'About'],
                               menu_icon='hospital-fill',
                               icons=['activity', 'heart', 'person', 'info-circle'],
                               default_index=0)

    # Display user name after login
    def display_username():
        if "user_name" in st.session_state:
            st.markdown(f"### Welcome, {st.session_state.user_name}!", unsafe_allow_html=True)

    # About Page
    if selected == "About":
        st.markdown("<h2 style='font-size: 40px; font-weight: bold;'>About Us</h2>", unsafe_allow_html=True)
        st.markdown("""
            <style>
                .about-text {
                    font-size: 24px;
                    font-weight: bold;
                }
                .about-table {
                    font-size: 20px;
                    border: 1px solid black;
                    border-collapse: collapse;
                    width: 100%;
                }
                .about-table th, .about-table td {
                    padding: 8px;
                    text-align: center;
                }
                .about-table th {
                    background-color: #f2f2f2;
                }
            </style>
            <div class="about-text">
                <p>This Multiple Disease Prediction System was devloped by:</p>
            </div>
            <table class="about-table">
                <tr>
                    <th>Name</th>
                    <th>USN</th>
                </tr>
                <tr>
                    <td><b>Abdul Musawwir</b></td>
                    <td><b>3BR22CS005</b></td>
                </tr>
                <tr>
                    <td><b>Akash G  </b></td>
                    <td><b>3BR22CS008</b></td>
                </tr>
                <tr>
                    <td><b>Amith Kumar</b></td>
                    <td><b>3BR22CS011</b></td>
                </tr>
                <tr>
                    <td><b>B V N Shanmukha </b></td>
                    <td><b>3BR22CS018</b></td>
                </tr>
            </table>
        """, unsafe_allow_html=True)
  

    # Diabetes Prediction Page
    if selected == 'Diabetes Prediction':
        st.title('Diabetes Prediction using ML')

        # getting the input data from the user
        col1, col2, col3 = st.columns(3)

        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')

        with col2:
            Glucose = st.text_input('Glucose Level in mg/dL (milligrams per deciliter)')

        with col3:
            BloodPressure = st.text_input('Blood Pressure value in mmHg (millimeters of mercury)')

        with col1:
            SkinThickness = st.text_input('Skin Thickness value in mm (millimeters)')

        with col2:
            Insulin = st.text_input('Insulin Level in mIU/L (micro International Units per liter)')

        with col3:
            BMI = st.text_input('BMI value in kg/m² (kilograms per square meter)')

        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

        with col2:
            Age = st.text_input('Age of the Person in years')

        # code for Prediction
        diab_diagnosis = ''

        # creating a button for Prediction
        if st.button('Diabetes Test Result'):
            user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                          BMI, DiabetesPedigreeFunction, Age]

            if check_empty_inputs(user_input):
                st.error("Please fill in all the fields before submitting.")
            else:
                try:
                    user_input = [float(x) for x in user_input]
                    diab_prediction = diabetes_model.predict([user_input])

                    if diab_prediction[0] == 1:
                        diab_diagnosis = 'The person is diabetic'
                    else:
                        diab_diagnosis = 'The person is not diabetic'
                except ValueError:
                    st.error("Invalid input. Please enter valid numeric values.")
                except Exception as e:
                    st.error(f"An error occurred during prediction: {e}")

        st.success(diab_diagnosis)

    # Heart Disease Prediction Page
    if selected == 'Heart Disease Prediction':
        st.title('Heart Disease Prediction using ML')

        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input('Age in years')

        with col2:
            sex = st.text_input('Sex')

        with col3:
            cp = st.text_input('Chest Pain types')

        with col1:
            trestbps = st.text_input('Resting Blood Pressure in mmHg (millimeters of mercury)')

        with col2:
            chol = st.text_input('Serum Cholestoral in mg/dl (milligrams per deciliter)')

        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl  (milligrams per deciliter)')

        with col1:
            restecg = st.text_input('Resting Electrocardiographic results')

        with col2:
            thalach = st.text_input('Maximum Heart Rate achieved in  beats per minute (bpm)' )

        with col3:
            exang = st.text_input('Exercise Induced Angina ')

        with col1:
            oldpeak = st.text_input('ST depression induced by exercise in mm(millimeters)')

        with col2:
            slope = st.text_input('Slope of the peak exercise ST segment')

        with col3:
            ca = st.text_input('Major vessels colored by flourosopy')

        with col1:
            thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

        # code for Prediction
        heart_diagnosis = ''

        # creating a button for Prediction
        if st.button('Heart Disease Test Result'):
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

            if check_empty_inputs(user_input):
                st.error("Please fill in all the fields before submitting.")
            else:
                try:
                    user_input = [float(x) for x in user_input]
                    heart_prediction = heart_disease_model.predict([user_input])

                    if heart_prediction[0] == 1:
                        heart_diagnosis = 'The person is having heart disease'
                    else:
                        heart_diagnosis = 'The person does not have any heart disease'
                except ValueError:
                    st.error("Invalid input. Please enter valid numeric values.")
                except Exception as e:
                    st.error(f"An error occurred during prediction: {e}")

        st.success(heart_diagnosis)

    # Parkinson's Prediction Page
