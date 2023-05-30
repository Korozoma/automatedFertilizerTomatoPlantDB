import os
import time
from datetime import datetime
from roboflow import Roboflow

rf = Roboflow(api_key="B0PWZV2z3c48JocEeeqk")
project = rf.workspace().project("tomato-fruit-detector-v2")
model = project.version(1).model

input_folder = 'Images/Captured'
output_folder = 'Images/AuditFruit'
text_data_folder = 'TextData'

# Create the output_folder and text_data_folder if they do not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if not os.path.exists(text_data_folder):
    os.makedirs(text_data_folder)

def get_processed_images(file_path):
    processed_images = set()
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith("------"):
                image_name = line.split(',')[0]
                processed_images.add(image_name)
    return processed_images

def process_image(image_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    month_date = datetime.now().strftime("%B %d")
    output_path = os.path.join(output_folder, f"prediction_{timestamp}_" + os.path.basename(image_path))
    prediction = model.predict(image_path, confidence=40, overlap=30)
    print(prediction.json())
    prediction.save(output_path)
    print(f"Prediction saved to {output_path}")

    # Save prediction width and height to a universal text file
    with open(os.path.join(text_data_folder, 'Fruit-Prediction_data.txt'), 'a') as file:
        image_name = os.path.basename(image_path)
        predictions = prediction.json()['predictions']
        for pred in predictions:
            width = pred['width']
            height = pred['height']
            file.write(f"{image_name}, {width}, {height}, {timestamp}, {month_date}, Fruit\n")  # Add comma after timestamp and date
        file.write("------\n")  # Add separator after predictions for each image

prediction_data_file = os.path.join(text_data_folder, 'Fruit-Prediction_data.txt')
if not os.path.exists(prediction_data_file):
    open(prediction_data_file, 'w').close()

processed_images = get_processed_images(prediction_data_file)

for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        file_path = os.path.join(input_folder, filename)
        if filename not in processed_images:
            print(f"Processing {file_path}")
            process_image(file_path)
            processed_images.add(filename)