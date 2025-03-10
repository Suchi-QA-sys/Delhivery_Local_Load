import json
import requests
import logging
from utils.config_loader import CONFIG
from utils.helpers import generate_curl

# Configure logging
logging.basicConfig(
    filename="attendance.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class CreateTracesModule:
    def __init__(self,client):
        base_url = CONFIG["base_url_primary"]
        self.create_traces_url = base_url + CONFIG["create_traces_endpoint"]
        self.client = client

    def create_traces(self, token, user_id, vehicle_number):
        if not token:
            logging.error("Error: No authentication token provided. Tracking request aborted.")
            print("Error: No authentication token provided. Tracking request aborted.")
            return

        headers = {
            "X-COREOS-ACCESS": token,
            "Content-Type": "application/json"
        }

        payload = {
            "user_id": user_id,
            "vehicle_number": vehicle_number
        }

        # Log the generated cURL command
        curl_command = generate_curl("POST", self.create_traces_url, headers, payload)
        logging.info(f"Generated cURL command: {curl_command}")
        print(f"Generated cURL: {curl_command}")

        try:
            response = self.client.post(self.smartphone_tracking_url, headers=headers, json=payload)

            if response.status_code == 200:
                logging.info("Smartphone tracking successful: %s", response.json())
                print("Smartphone tracking successful:", response.json())
            else:
                logging.error("Error in smartphone tracking. Status Code: %s, Response: %s", response.status_code, response.text)
                print(f"Error in smartphone tracking: {response.status_code}, Response: {response.text}")

        except self.client.RequestException as e:
            logging.exception("Error occurred while making tracking request: %s", str(e))
            print("Error: Unable to track smartphone. Please check logs for details.")