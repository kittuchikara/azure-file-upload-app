from flask import Flask, render_template, request
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

STORAGE_CONNECTION = os.getenv("STORAGE_CONNECTION")

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

    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=file.filename
    )

    blob_client.upload_blob(file, overwrite=True)

    return f"{file.filename} uploaded successfully."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)