data_file = "TextData/convertedCM.txt"

def calculate_days_to_reach_target(data):
    incremental_sum = 0
    increment_count = 0

    for value, _ in data:
        if value < 30:
            incremental_sum += value
            increment_count += 1

    if increment_count == 0:
        return None

    average_increment = incremental_sum / increment_count
    target_value = 30
    increments_to_reach_target = target_value - average_increment

    if increments_to_reach_target <= 0:
        return 0

    days_to_reach_target = increments_to_reach_target / average_increment
    return int(days_to_reach_target)

def main():
    stem_data = []

    with open(data_file, 'r') as file:
        for line in file:
            if "Stem" in line:
                parts = line.split(":")
                value = float(parts[1].split(",")[0].strip())
                stem_data.append((value, "Stem"))

    days_to_reach_30 = calculate_days_to_reach_target(stem_data)
    
    if days_to_reach_30 is not None:
        print(f"It will take approximately {days_to_reach_30} days to reach a value of 30.")
    else:
        print("No data points less than 30 were found.")

if __name__ == "__main__":
    main()