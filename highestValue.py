import os

def check_duplicates(output_file_path, image_name):
    if not os.path.exists(output_file_path):
        return False

    with open(output_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip().startswith(image_name):
                return True
    return False

def extract_max_dimension(input_file_path, output_file_path, file_mode):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
        new_image = True

        with open(output_file_path, file_mode) as output_file:
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

                if check_duplicates(output_file_path, image_name):
                    continue

                if new_image:
                    if not lines.index(line) == 0:
                        output_file.write('------\n')
                    new_image = False

                output_file.write(f"{image_name}: {max_dimension}, {leaf_label}\n")

            if not new_image:
                output_file.write('------\n')

# Replace the file paths if necessary
input_file_path1 = 'TextData/Leaf-Prediction_data.txt'
output_file_path1 = 'TextData/leaf_highValue.txt'
extract_max_dimension(input_file_path1, output_file_path1, file_mode='a')

input_file_path3 = 'TextData/Stem-Prediction_data.txt'
output_file_path3 = 'TextData/stem_highValue.txt'
extract_max_dimension(input_file_path3, output_file_path3, file_mode='a')

input_file_path2 = 'TextData/Fruit-Prediction_data.txt'
output_file_path2 = 'TextData/fruit_highValue.txt'
extract_max_dimension(input_file_path2, output_file_path2, file_mode='a')
