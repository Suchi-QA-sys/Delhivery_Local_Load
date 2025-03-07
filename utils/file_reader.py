import json 
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_latest_entry_with_value(json_file,avoid_value):
    try:
        with open(json_file, "r") as file:
            data = json.load(file)

        unsynced_entries = {k: v for k, v in data.items() if v != avoid_value}
        if not unsynced_entries:
            logger.warning(f"No available drivers found with status not equal to {avoid_value}.")
            return None

        latest_driver_id = max(unsynced_entries, key=lambda k: data[k])
        return latest_driver_id

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error reading JSON file: {e}")
        return None