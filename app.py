import streamlit as st
import pickle
import numpy as np


# --- Function to load the model and encoders ---
@st.cache_resource
def load_model():
    """Loads the saved model package from disk."""
    try:
        with open("salary_model.pkl", "rb") as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        st.error("Model file not found. Please run 'prepare_assets.py' first.")
        return None


# --- Load the model and necessary encoders ---
model_data = load_model()

if model_data:
    model = model_data["model"]
    le_country = model_data["le_country"]
    le_education = model_data["le_education"]

    # --- Page Configuration ---
    st.set_page_config(page_title="Salary Predictor", page_icon="💼", layout="wide")

    # --- Page Title and Description ---
    st.title("👨‍💻 Software Developer Salary Predictor")
    st.markdown(
        """
    Welcome to the Salary Prediction App! This tool uses a machine learning model, trained on data from the Stack Overflow Developer Survey, to estimate developer salaries.
    
    **Instructions:**
    1.  Select a **Country**.
    2.  Choose the highest **Education Level** achieved.
    3.  Specify your **Years of Professional Coding Experience**.
    4.  Click the **"Predict Salary"** button to see the estimated annual salary in USD.
    """
    )

    # --- User Input Section ---
    st.header("Enter Your Details")

    # Create columns for a cleaner layout
    col1, col2, col3 = st.columns(3)

    with col1:
        country_options = tuple(le_country.classes_)
        country = st.selectbox("Country", country_options)

    with col2:
        education_options = tuple(le_education.classes_)
        education = st.selectbox("Education Level", education_options)

    with col3:
        experience = st.slider("Years of Experience", 0, 50, 5)  # Min, Max, Default

    # --- Prediction Logic ---
    if st.button("Predict Salary", type="primary", use_container_width=True):
        try:
            # Transform inputs using the loaded encoders
            country_encoded = le_country.transform([country])[0]
            education_encoded = le_education.transform([education])[0]

            # Create feature array for prediction
            X_input = np.array([[country_encoded, education_encoded, experience]])

            # Make prediction
            predicted_salary = model.predict(X_input)[0]

            # Display result with flair
            st.success("Prediction successful!")
            st.metric(
                label="Estimated Annual Salary (USD)",
                value=f"${predicted_salary:,.2f}",
                help="This is an estimate based on the model's training data.",
            )
            st.balloons()

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
