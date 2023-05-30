import pymongo

# Define the conversion factor
conversion_factor = 9.05

# Read the input file
with open('TextData/highest_values.txt', 'r') as file:
    lines = file.readlines()

# Process the lines and perform the conversion
converted_lines = []
for line in lines:
    line = line.strip()
    if line == "------":
        continue
    
    parts = line.split(': ')
    if len(parts) != 2:
        # Skip lines that don't match the expected format
        continue
    
    image_name = parts[0]
    value_attr = parts[1].split(', ')
    if len(value_attr) != 3:
        # Skip lines that don't match the expected format
        continue
    
    value = value_attr[0]
    attribute = value_attr[1]
    converted_value = float(value) / conversion_factor
    converted_line = f"{image_name}: {converted_value:.2f}, {attribute}"
    converted_lines.append(converted_line)

# Save the converted lines to a new file
with open('TextData/convertedCM.txt', 'w') as file:
    file.write('\n'.join(converted_lines))

# Connect to MongoDB
client = pymongo.MongoClient('mongodb+srv://rver:AdSDJzoTvcpJEd6X@researchtomatodatabase.wrbn0fd.mongodb.net/')
db = client['parameterData']
collection = db['convertedCM']

# Read the converted file
with open('TextData/convertedCM.txt', 'r') as file:
    converted_text = file.read()

# Replace the existing file in MongoDB
data = {
    'file_name': 'convertedCM.txt',
    'content': converted_text
}
filter_query = {'file_name': 'convertedCM.txt'}
collection.replace_one(filter_query, data, upsert=True)

# Close the MongoDB connection
client.close()
