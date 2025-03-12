import json
import requests
import logging
from utils.config_loader import CONFIG
from utils.helpers import generate_curl
from utils.file_writer import update_json_value,append_to_json

# Configure logging
logging.basicConfig(
    filename="broadcast_lists.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class BroadCastActionModule:
    def __init__(self, client):
        base_url = CONFIG["base_url_primary"]
        self.get_broadcast_action_url = base_url + CONFIG["get_broadcast_action_endpoint"]
        self.client = client

    def punch_broadcast_action(self, token, allocation_id, broadcast_id, rider_id, realloted=False):
        if not token:
            logging.error("Error: No authentication token provided. Broadcast lists request aborted.")
            print("Error: No authentication token provided. Broadcast lists request aborted.")
            return

        headers = {
            "X-COREOS-ACCESS": token,
            "Content-Type": "application/json",
            "X-COREOS-TID": "delvjkninl"
        }
        
        payload = {
            "allocation_id": allocation_id,
            "broadcast_id": broadcast_id,
            "driver_id":rider_id,
            "action": "accept"
        }

        curl_command = generate_curl("POST", self.get_broadcast_action_url, headers, payload)
        logging.info(f"Generated cURL command: {curl_command}")
        print(f"Generated cURL: {curl_command}")

        try:
            response = self.client.post(self.get_broadcast_action_url, headers=headers, json=payload)

            if response.status_code == 200:
                logging.info("Broadcast Action Punched successfully: %s", response.json())
                print("Broadcast Action Punched successfully:", response.json())
                if realloted:
                    update_json_value("riderID_broadcastID_mapping",rider_id,broadcast_id)
                else:
                    append_to_json("riderID_broadcastID_mapping", rider_id, broadcast_id)
            else:
                logging.error("Error in broadcast action punch. Status Code: %s, Response: %s", response.status_code, response.text)
                print(f"Error in Broadcast action Punch: {response.status_code}, Response: {response.text}")

        except requests.RequestException as e:
            logging.exception("Error occurred while making Broadcast Action request: %s", str(e))
            print("Error: Unable to punch Broadcast Action. Please check logs for details.")
