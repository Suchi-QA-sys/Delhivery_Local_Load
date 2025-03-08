import json 
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_latest_entry_with_value(file_name,value,avoid_values):
    file_path = f"{file_name}.json"
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