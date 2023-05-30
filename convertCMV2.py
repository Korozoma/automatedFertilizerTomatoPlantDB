# Function to convert centimeters and append to file
def convert_cm(file_path, output_file):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    converted_data = []
    for line in lines:
        if '------' in line:
            continue  # Ignore separator line

        values = line.strip().split(', ')
        if len(values) >= 6:
            file_name = values[0]
            converted_values = [float(values[1]) / 9.05, float(values[2]) / 9.05]  # Convert 2nd and 3rd elements to floats
            label = values[5]  # Extract the label from the 6th element
            converted_line = f'{file_name}, {", ".join(map(str, converted_values))}, {label}\n'

            if converted_line not in converted_data:
                converted_data.append(converted_line)

    with open(output_file, 'a+') as file:  # Use 'a+' mode for reading and appending to the output file
        file.seek(0)  # Move the file pointer to the beginning
        existing_data = file.read()

        file.seek(0, 2)  # Move the file pointer to the end
        for line in converted_data:
            if line not in existing_data:
                file.write(line)

# Process Fruit-Prediction_data.txt
convert_cm('TextData/Fruit-Prediction_data.txt', 'TextData/convertedCMV2.txt')

# Process Leaf-Prediction_data.txt
convert_cm('TextData/Leaf-Prediction_data.txt', 'TextData/convertedCMV2.txt')

# Process Stem-Prediction_data.txt
convert_cm('TextData/Stem-Prediction_data.txt', 'TextData/convertedCMV2.txt')
