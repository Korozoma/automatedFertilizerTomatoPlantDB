import requests
import datetime
from pymongo import MongoClient

# Set up the camera stream URL
stream_url = "http://192.168.1.12:8080/shot.jpg"  # Replace with your phone's IP address and port number

# MongoDB connection settings
mongodb_url = "mongodb+srv://rver:AdSDJzoTvcpJEd6X@researchtomatodatabase.wrbn0fd.mongodb.net/"  # Replace with your MongoDB connection URL
database_name = "capturedImage"  # Replace with your database name
collection_name = "Images"  # Replace with your collection name

try:
    # Request the image from the camera stream
    response = requests.get(stream_url)

    if response.status_code == 200:
        # Generate a unique file name using the current date and time
        current_datetime = datetime.datetime.now()
        file_name = current_datetime.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"

        # Specify the destination folder where you want to save the image
        destination_folder = "Images/Captured"

        # Save the captured image to the destination folder with the unique file name
        destination_path = f"{destination_folder}/{file_name}"
        with open(destination_path, "wb") as file:
            file.write(response.content)

        print("Image saved to the local folder:", destination_path)

        # Upload the image to MongoDB
        client = MongoClient(mongodb_url)
        database = client[database_name]
        collection = database[collection_name]
        with open(destination_path, "rb") as file:
            image_data = file.read()
        image_document = {"filename": file_name, "image": image_data}
        result = collection.insert_one(image_document)

        print("Image uploaded to MongoDB with document ID:", result.inserted_id)

    else:
        raise ValueError("Failed to retrieve image from the camera stream.")

except Exception as e:
    print("An error occurred:", str(e))
