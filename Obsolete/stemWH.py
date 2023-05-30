import os

def extract_max_dimension(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
        new_image = True

        with open(output_file_path, 'w') as output_file:
            for line in lines:
                if line.strip() == '------':
                    new_image = True
                    continue

                data = line.strip().split(', ')
                image_name = data[0]
                width = float(data[1])
                height = float(data[2])
                max_dimension = max(width, height)
                leaf_label = data[-1]

                if new_image:
                    if not lines.index(line) == 0:
                        output_file.write('------\n')
                    new_image = False

                output_file.write(f"{image_name}: {max_dimension}, {leaf_label}\n")

            if not new_image:
                output_file.write('------\n')

# Replace the file paths if necessary
input_file_path = 'TextData/Stem-Prediction_data.txt'
output_file_path = 'TextData/stem_highValue.txt'

extract_max_dimension(input_file_path, output_file_path)