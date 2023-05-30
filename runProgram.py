import subprocess
from time import sleep
from datetime import datetime, time, timedelta

# Variable to keep track of whether camera capture and image retrieval have already run
camera_capture_done = False
get_image_mongo_done = False

while True:
    # Get the current time
    now = datetime.now().time()

    # Check if it's between 8:00 am and 8:30 am
    if time(8, 0) <= now <= time(8, 30):
        # Run the Python files in the specified order
        if not camera_capture_done:
            subprocess.run(["python", "cameraCapture.py"])
            camera_capture_done = True

        if not get_image_mongo_done:
            subprocess.run(["python", "getImageMongoDB.py"])
            get_image_mongo_done = True

        subprocess.run(["python", "autoMeasureStem.py"])
        subprocess.run(["python", "autoMeasureLeaf.py"])
        subprocess.run(["python", "autoMeasureFruit.py"])
        subprocess.run(["python", "highestValue.py"])
        subprocess.run(["python", "compileData.py"])
        subprocess.run(["python", "convertCM.py"])
        subprocess.run(["python", "stageDetermine.py"])
        
    # Check if it's between 8:40 am and 9:00 am
    elif time(8, 40) <= now <= time(9, 0):
        camera_capture_done = False
        get_image_mongo_done = False

        # Run the Python files in the specified order
        if not camera_capture_done:
            subprocess.run(["python", "cameraCapture.py"])
            camera_capture_done = True

        if not get_image_mongo_done:
            subprocess.run(["python", "getImageMongoDB.py"])
            get_image_mongo_done = True

        subprocess.run(["python", "autoMeasureStem.py"])
        subprocess.run(["python", "autoMeasureLeaf.py"])
        subprocess.run(["python", "autoMeasureFruit.py"])
        subprocess.run(["python", "highestValue.py"])
        subprocess.run(["python", "compileData.py"])
        subprocess.run(["python", "convertCM.py"])
        subprocess.run(["python", "stageDetermine.py"])

    # Check if it's between 9:10 am and 9:30 am
    elif time(9, 10) <= now <= time(9, 30):
        camera_capture_done = False
        get_image_mongo_done = False
        
        # Run the Python files in the specified order
        if not camera_capture_done:
            subprocess.run(["python", "cameraCapture.py"])
            camera_capture_done = True

        if not get_image_mongo_done:
            subprocess.run(["python", "getImageMongoDB.py"])
            get_image_mongo_done = True

        subprocess.run(["python", "autoMeasureStem.py"])
        subprocess.run(["python", "autoMeasureLeaf.py"])
        subprocess.run(["python", "autoMeasureFruit.py"])
        subprocess.run(["python", "highestValue.py"])
        subprocess.run(["python", "compileData.py"])
        subprocess.run(["python", "convertCM.py"])
        subprocess.run(["python", "stageDetermine.py"])

    # Sleep for a few seconds before checking the time again
    sleep(5)

    # Reset the flags at the start of a new day
    if now < time(8, 0):
        camera_capture_done = False
        get_image_mongo_done = False

    # Calculate the time until the next hour
    next_hour = datetime.now() + timedelta(hours=1)
    next_hour = next_hour.replace(minute=0, second=0, microsecond=0)
    sleep_time = (next_hour - datetime.now()).total_seconds()

    # Calculate the time until 8:00 am the next day
    tomorrow = datetime.now().date() + timedelta(days=1)
    next_run_time = datetime.combine(tomorrow, time(8, 0))
    time_until_8am = (next_run_time - datetime.now()).total_seconds()

    # Output the remaining time in hours
    hours_remaining = sleep_time / 3600
    hours_until_8am = time_until_8am / 3600
    print("Sleeping for {:.2f} hours until the next hour. {:.2f} hours until 8:00 am".format(hours_remaining, hours_until_8am))

    # Wait until the next hour
    sleep(sleep_time)

    # Continue with the loop to check if it's 8:00 am