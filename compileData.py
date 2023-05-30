import os
from datetime import datetime

def gather_highest_value(input_file_path, output_file_path, file_mode='w'):
    current_time = datetime.now()
    formatted_date = current_time.strftime("%B %d %I:%M %p")  # Ex: March 12 08:00 AM

    with open(input_file_path, 'r') as file:
        lines = file.readlines()
        new_image = True

        with open(output_file_path, file_mode) as output_file:
            image_values = {}

            for line in lines:
                if line.strip() == '------':
                    if len(image_values) > 0:
                        for image_name, (max_value, label) in image_values.items():
                            output_file.write(f"{image_name}: {max_value}, {label}, {formatted_date}\n")
                        output_file.write('------\n')
                    image_values = {}
                    new_image = True
                    continue

                data = line.strip().split(': ')
                if len(data) < 2:
                    continue  # Skip lines with insufficient elements

                image_name = data[0]
                try:
                    value = float(data[1].split(',')[0])
                    label = data[1].split(',')[1].strip()
                except (ValueError, IndexError):
                    continue  # Skip lines with non-numeric values or incorrect format

                if new_image or image_name not in image_values or value > image_values[image_name][0]:
                    image_values[image_name] = (value, label)
                    new_image = False

            if len(image_values) > 0:
                for image_name, (max_value, label) in image_values.items():
                    output_file.write(f"{image_name}: {max_value}, {label}, {formatted_date}\n")
                output_file.write('------\n')

# Replace the file paths if necessary
output_file_path = 'TextData/highest_values.txt'

input_file_path1 = 'TextData/leaf_highValue.txt'
gather_highest_value(input_file_path1, output_file_path, file_mode='w')

input_file_path2 = 'TextData/stem_highValue.txt'
gather_highest_value(input_file_path2, output_file_path, file_mode='a')

input_file_path3 = 'TextData/fruit_highValue.txt'
gather_highest_value(input_file_path3, output_file_path, file_mode='a')