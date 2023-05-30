import datetime
import pymongo
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Open the file for reading
with open('TextData/convertedCM.txt', 'r') as file:
    data = file.readlines()

# Initialize variables for each label
leaf_value = None
stem_value = None
fruit_value = None

# Iterate over the data in reverse order
for line in reversed(data):
    parts = line.strip().split(': ')
    if len(parts) != 2:
        continue

    filename, rest = parts[0], parts[1]
    value, label = rest.split(', ')
    value = float(value)

    # Update the latest value for the current label if it's the first encountered
    if label == 'Leaf' and leaf_value is None:
        leaf_value = value
    elif label == 'Stem' and stem_value is None:
        stem_value = value
    elif label == 'Fruit' and fruit_value is None:
        fruit_value = value

    # Break the loop if all labels have at least one value
    if leaf_value is not None and stem_value is not None and fruit_value is not None:
        break

# Print the latest values
print("Latest Leaf Value:", leaf_value)
print("Latest Stem Value:", stem_value)
print("Latest Fruit Value:", fruit_value)

# Check the conditions and determine the corresponding stage
if 5 <= stem_value <= 19:
    if leaf_value is not None and 3 <= leaf_value <= 9:
        stage = "Sapling"
    else:
        stage = "Sapling (Leaf)"
elif 20 <= stem_value <= 29:
    if leaf_value is not None and leaf_value >= 10:
        stage = "Flowering"
    else:
        stage = "Flowering (Leaf)"
elif stem_value is not None and stem_value > 30:
    if fruit_value is not None:
        stage = "Fruit"
    else:
        stage = "Fruit (Developing)"
else:
    stage = "Unknown"

# Get the current date in the "Month Day" format
current_date = datetime.datetime.now().strftime("%B %d")

# Format the stage with date
stage_with_date = f"{stage} ({current_date})"

# Save the stage to the local file "currentGrowthStage.txt"
with open("TextData/currentGrowthStage.txt", "w") as file:
    file.write(stage_with_date)

# Print the stage and date
print(stage_with_date)

# MongoDB connection settings
mongo_uri = 'mongodb+srv://rver:AdSDJzoTvcpJEd6X@researchtomatodatabase.wrbn0fd.mongodb.net/'
database_name = 'parameterData'
collection_name = 'growthStage'

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
database = client[database_name]
collection = database[collection_name]

# Check if the document already exists in MongoDB
existing_document = collection.find_one()

if existing_document:
    # Update the existing document with the new growth stage
    filter_query = {}  # Add filter criteria if needed
    update_query = {
        '$set': {
            'growth_stage': stage
        }
    }
    
    collection.update_one(filter_query, update_query)
    print("Existing document updated!")
else:
    # Create a new document with the growth stage
    document = {
        'growth_stage': stage
    }
    
    collection.insert_one(document)
    print("New document inserted!")

# Print the updated document ID
updated_document = collection.find_one()
print("Updated Document ID:", updated_document['_id'])
print("Updated Document:")
print(updated_document)

# Google Sheets connection settings
credentials = ServiceAccountCredentials.from_json_keyfile_name('researchprojectgrowth-5ec60156b11a.json', ['https://www.googleapis.com/auth/spreadsheets'])
google_sheets_id = '1BZJxVbcTFnRLpS3dP8ZBzBPfN0YmztBO_6jLP4di9hc'
worksheet_name = 'growth'

# Connect to Google Sheets
client = gspread.authorize(credentials)
sheet = client.open_by_key(google_sheets_id).worksheet(worksheet_name)

# Save the stage to cell B1 of the sheet "growth"
sheet.update('B1', stage_with_date)

print("Data uploaded to Google Sheets!")

