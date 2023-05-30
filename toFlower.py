from datetime import datetime

# Read the file and extract relevant data
data = []
with open('TextData/convertedCM.txt', 'r') as file:
    for line in file:
        if 'Stem' in line:
            parts = line.split(':')
            value = float(parts[1].split(',')[0])
            date_str = parts[0].split('_')[0]
            date = datetime.strptime(date_str, '%Y-%m-%d')
            data.append((date, value))

# Sort the data by date
data.sort(key=lambda x: x[0])

# Calculate the number of days to reach 30cm based on the last recorded date
last_date, last_value = data[-1]
days_to_30cm = (30 - last_value) / ((last_value - data[0][1]) / (last_date - data[0][0]).days)

# Calculate the growth rate
initial_value = data[0][1]
growth_rate = (last_value - initial_value) / (last_date - data[0][0]).days

# Append the filtered data, days to reach 30cm, growth rate, and current growth stage in the existing file
with open('TextData/PredictedDays.txt', 'a') as output_file:
    output_file.write("\n" + "-" * 50 + "\n")
    output_file.write("Data between 20cm and 30cm:\n")
    for date, value in data:
        if 20 <= value <= 30:
            output_file.write(f"{date.date()}: {value}\n")
    output_file.write(f"{last_date.date()}: {days_to_30cm:.0f} days remaining\n")
    output_file.write(f"Growth Rate: {growth_rate:.2f} cm/day\n")
    output_file.write("Current Growth Stage: Flowering Stage\n")

print("Prediction appended in PredictedDays.txt")
