import json 
import logging
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_latest_entry_with_value(file_name,value,avoid_values):
    # Ensure the "data" directory exists
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    # Define the full file path inside the "data" directory
    file_path = os.path.join(data_dir, f"{file_name}.json")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        unsynced_entries = {k: v for k, v in data.items() if v == value and k not in avoid_values}
        logger.info(f"Avoid List is: {avoid_values}")
        if not unsynced_entries:
            logger.warning(f"No available drivers found with status not equal to {value}.")
            return None
        
        logger.info(f"unsynced entries left{unsynced_entries}")

        latest_driver_id = max(unsynced_entries, key=lambda k: data[k])
        return latest_driver_id

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error reading JSON file: {e}")
        return None

def get_json_entries_based_on_index(file_name, index,directory_name="data"):

    data_dir = directory_name
    os.makedirs(data_dir, exist_ok=True)

    # Define the full file path inside the "data" directory
    file_path = os.path.join(data_dir, f"{file_name}.json")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        # Ensure data is a dictionary
        if not isinstance(data, dict):
            logger.error("Invalid JSON structure: Expected a dictionary.")
            return None

        # Convert dictionary items into a list
        items_list = list(data.items())

        # Check if index is within range
        if index < 0 or index >= len(items_list):
            logger.error(f"Index {index} is out of range.")
            return None

        # Fetch the key-value pair at the specified index
        result = list(items_list[index])

        logger.info(f"Extracted key-value pair at index {index}: {result}")
        return result

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error reading JSON file: {e}")
        return None
