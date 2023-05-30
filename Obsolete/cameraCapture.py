import requests
import datetime

# Set up the camera stream URL
stream_url = "http://192.168.1.5:8080/shot.jpg"  # Replace with your phone's IP address and port number

try:
    # Request the image from the camera stream
    response = requests.get(stream_url)

    if response.status_code == 200:
        # Generate a unique file name using the current date and time
        current_datetime = datetime.datetime.now()
        file_name = current_datetime.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"

        # Specify the destination folder where you want to save the image
        destination_folder = "Images/Phone"

        # Save the captured image to the destination folder with the unique file name
        destination_path = f"{destination_folder}/{file_name}"
        with open(destination_path, "wb") as file:
            file.write(response.content)

        print("Image saved to the local folder:", destination_path)

    else:
        raise ValueError("Failed to retrieve image from the camera stream.")

except Exception as e:
    print("An error occurred:", str(e))
