from flask import Flask, render_template, request
from azure.storage.blob import BlobServiceClient
from config import get_secret
import pyodbc

app = Flask(__name__)

STORAGE_CONNECTION = get_secret("StorageConnectionString")
SQL_CONNECTION = get_secret("SqlConnectionString")

CONTAINER_NAME = "uploads"

blob_service_client = BlobServiceClient.from_connection_string(
    STORAGE_CONNECTION
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return "No file selected"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    # Upload file to Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=file.filename
    )

    blob_client.upload_blob(file, overwrite=True)

    # Get Blob URL
    blob_url = blob_client.url

    # Store file details in Azure SQL Database
    try:
        conn = pyodbc.connect(SQL_CONNECTION)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO UploadedFiles (FileName, BlobUrl)
            VALUES (?, ?)
            """,
            file.filename,
            blob_url
        )

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        return f"File uploaded to Blob Storage, but database insert failed.<br><br>{e}"

    return f"{file.filename} uploaded successfully."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)