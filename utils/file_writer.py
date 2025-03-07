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
    file_path = f"{file_name}.json"
    try:
        # Try to load existing JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("File not found or empty. Cannot update.")
        return

    if key in data:
        data[key] = new_value
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Updated '{key}' to '{new_value}' in {file_name}.")
    else:
        print(f"Key '{key}' not found in {file_name}.")
        

