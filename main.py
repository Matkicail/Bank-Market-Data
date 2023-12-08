from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from interpret import init_show_server, get_show_addr
from interpret.glassbox import ExplainableBoostingClassifier
from fastapi import HTTPException
import pandas as pd
import pickle
from helpers.processing import process_columns, encode_data, explain_errors
import os

app = FastAPI()
training_cols = pd.read_csv("./data/processed.csv").columns
with open("./model/ebm_model.pkl", "rb") as file:
    ebm_model = pickle.load(file)
    ip_address = "localhost"
    port = 8001
    init_show_server(addr=(ip_address, port))

    init_show_server(addr=(ip_address, port))

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read the file into a DataFrame
        df = pd.read_csv(file.file, delimiter=";")
        dummy_cols = [
            "job",
            "marital",
            "default",
            "education",
            "housing",
            "loan",
            "contact",
            "month",
            "day_of_week",
            "poutcome",
            "pdays",
            "campaign",
        ]
        data = process_columns(df)
        data = encode_data(data, dummy_cols, training_columns=training_cols)
        predictions = ebm_model.predict(data)
        probabilities = ebm_model.predict_proba(data)
        predictions_list = predictions.tolist()
        probabilities_list = probabilities.tolist()
        explanation = ebm_model.explain_local(data, predictions)

        # Create a directory to store HTML files if it doesn't exist
        if not os.path.exists("html_files"):
            os.makedirs("html_files")

        show_link = f"http://{ip_address}:{port}/"
        # show_link = None
        print(show_link)

        return {
            "message": "File processed successfully",
            "prediction": predictions_list,
            "probabilities": probabilities_list,
            "link": show_link,  # Provide the link to the HTML file
        }

    except ValueError as e:
        explain_errors()
        return {"message": f"Error in processing: {str(e)}"}
    except Exception as e:
        # Catching any other exceptions
        explain_errors()
        return {"message": f"Unexpected error: {str(e)}"}
