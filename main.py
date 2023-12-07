import streamlit as st
import pandas as pd
import requests
import json

# Function to call FastAPI for predictions
def get_predictions(data):
    
    # Convert the DataFrame to a list of dictionaries
    data_json = data.to_dict(orient='records')

    # Make the POST request with JSON data
    response = requests.post("http://localhost:8000/predict", json={'data': data_json})
    return response.json()

# Initialize session state variables
if 'data_uploaded' not in st.session_state:
    st.session_state['data_uploaded'] = False

# Title
st.title("My Dynamic Streamlit App")

# File Uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    st.session_state['data_uploaded'] = True
    # Process the file...

# Predict button
if st.button("Predict"):
    if st.session_state['data_uploaded']:
        # Perform prediction
        predictions = get_predictions(pd.read_csv(uploaded_file))
        st.write("Prediction results...")
    else:
        st.warning("Please upload a file to make predictions.")

# Conditional content based on session state
if st.session_state['data_uploaded']:
    st.write("File has been uploaded. Ready to predict!")
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview:")
    st.dataframe(data.head())
else:
    st.write("Awaiting file upload.")
