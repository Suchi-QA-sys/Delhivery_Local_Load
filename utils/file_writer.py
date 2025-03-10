def write_to_file(file_name, content):
    file_path = f"{file_name}.txt"

    with open(file_path, "a") as file:  # Open in append mode
        file.write(content + "\n")

    print(f"✅ Content written to {file_path}")

import json

def append_to_json(file_name, key, value):
    file_path = f"{file_name}.json"
    try:
        # Try to load existing JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}  

    data[key] = value

    # Write back to file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_json_value(file_name, key, new_value):
    try:
        with open(f"{file_name}.json", "r+") as file:
            data = json.load(file)

            if key in data:
                data[key] = new_value  # Update value

                file.seek(0)  # Move cursor to the beginning
                json.dump(data, file, indent=4)
                file.truncate()  # Ensure no old data remains

        # Add an explicit flush to force writing changes
        with open(f"{file_name}.json", "r") as verify_file:
            json.load(verify_file)  # Ensures the file is fully written before proceeding

    except Exception as e:
        print(f"Error updating JSON file: {e}")
        

