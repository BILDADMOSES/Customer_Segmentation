from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
from data_processing import preprocess_and_cluster
from utilities import secure_filename, check_required_fields
from csv_uploader import create_table_from_csv

app = FastAPI()

UPLOAD_FOLDER = "./data"
ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    """
    Checks if the uploaded file has an allowed extension.

    Parameters:
    - filename: The name of the file.

    Returns:
    - True if the file has an allowed extension, False otherwise.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Uploads a file to the server.

    Parameters:
    - file: The file to upload.

    Returns:
    - A message indicating whether the upload was successful or not.
    """
    try:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            contents = await file.read()
            with open(os.path.join(UPLOAD_FOLDER, "data.csv"), "wb") as f:
                f.write(contents)
            required_fields = [
                "Dt_Customer",
                "Year_Birth",
                "MntWines",
                "MntFruits",
                "MntMeatProducts",
                "MntFishProducts",
                "MntSweetProducts",
                "MntGoldProds",
                "Marital_Status",
                "Kidhome",
                "Teenhome",
                "Education",
                "AcceptedCmp1",
                "AcceptedCmp2",
                "AcceptedCmp3",
                "AcceptedCmp4",
                "AcceptedCmp5",
                "Complain",
                "Response",
                "ID",
                "Z_CostContact",
                "Z_Revenue",
                "Income",
            ]
            missing_fields = check_required_fields("./data/data.csv", required_fields)
            if missing_fields:
                raise HTTPException(
                    status_code=400,
                    detail=f"The following required fields are missing: {', '.join(missing_fields)}",
                )

            return JSONResponse(
                status_code=200, content={"message": "File uploaded successfully"}
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid file type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@app.get("/process-data")
async def download_images():
    """
    Processes the uploaded data and returns a zip file of the results.

    Returns:
    - A zip file of the processed data.
    """
    try:
        input_data_path = "./data/data.csv"
        preprocess_and_cluster(input_data_path)
        shutil.make_archive("results", "zip", "./results")
        return FileResponse("results.zip", media_type="application/zip")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@app.get("/download-csv")
async def download_csv():
    """
    Downloads the uploaded CSV file.

    Returns:
    - The uploaded CSV file.
    """
    try:
        csv_path = "./data/data.csv"  # replace with your csv path
        return FileResponse(csv_path, media_type="text/csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@app.post("/save-to-db")
async def save_to_db():
    """
    Saves the uploaded data to the database.

    Returns:
    - A message indicating whether the data was saved successfully or not.
    """
    try:
        create_table_from_csv("./data/data.csv", "customers")
        return JSONResponse(
            status_code=200, content={"message": "Data saved to database successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
