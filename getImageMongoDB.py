import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection settings
mongodb_url = "mongodb+srv://rver:AdSDJzoTvcpJEd6X@researchtomatodatabase.wrbn0fd.mongodb.net/"  # Replace with your MongoDB connection URL
database_name = "capturedImage"  # Replace with your database name
collection_name = "Images"  # Replace with your collection name

# Local directory path to save the downloaded images
local_directory_path = "Images/Captured"  # Replace with your desired local directory path

# Connect to MongoDB
client = MongoClient(mongodb_url)
database = client[database_name]
collection = database[collection_name]

# Get the list of all file documents in the collection
file_documents = collection.find()

# Iterate over each file document
for file_doc in file_documents:
    # Get the file ID and filename
    file_id = str(file_doc["_id"])
    filename = file_doc["filename"]

    # Local file path to save the downloaded image
    local_file_path = f"{local_directory_path}/{filename}"

    # Check if the file already exists locally
    if not os.path.exists(local_file_path):
        # Get the image binary data
        image_data = file_doc["image"]

        # Save the file to the local file path
        with open(local_file_path, "wb") as f:
            f.write(image_data)

        print("Image downloaded and saved to:", local_file_path)
    else:
        print("Image already downloaded:", local_file_path)
