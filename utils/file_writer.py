import os
import json


def write_to_file(file_name, content):
    # Ensure the "data" directory exists
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    # Define the full file path inside the "data" directory
    file_path = os.path.join(data_dir, f"{file_name}.txt")

    with open(file_path, "a") as file:  # Open in append mode
        file.write(content + "\n")

    print(f"✅ Content written to {file_path}")


def append_to_json(file_name, key, value):
    # Ensure the "data" directory exists
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    # Define the full file path inside the "data" directory
    file_path = os.path.join(data_dir, f"{file_name}.json")
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
        # Ensure the "data" directory exists
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
    
        # Define the full file path inside the "data" directory
        file_path = os.path.join(data_dir, f"{file_name}.json")
        with open(file_path, "r+") as file:
            data = json.load(file)

            if key in data:
                data[key] = new_value  # Update value

                file.seek(0)  # Move cursor to the beginning
                json.dump(data, file, indent=4)
                file.truncate()  # Ensure no old data remains

        
        with open(f"{file_name}.json", "r") as verify_file:
            json.load(verify_file)  

    except Exception as e:
        print(f"Error updating JSON file: {e}")
        

