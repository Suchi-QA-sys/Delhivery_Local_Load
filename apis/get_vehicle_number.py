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



class GetVehicleNumberModule:
    def __init__(self,client):
        base_url = CONFIG["base_url_primary"]
        self.get_vehicle_url = base_url + CONFIG["get_vehicle_number_endpoint"]
        self.client = client

    def get_vehicle_number(self, token, vehicle_id):
        if not token:
            logging.error("Error: No authentication token provided. Tracking request aborted.")
            print("Error: No authentication token provided. Tracking request aborted.")
            return

        headers = {
            "X-COREOS-ACCESS": token,
            "Content-Type": "application/json",
            "X-COREOS-TID": "delvjkninl",
            "X-COREOS-USERINFO":json.dumps({"user":"rudra","id":"platform:app:service:86e306d4-564c-5082-90b5-a7ad29fb3579"})
        }

        # Log the generated cURL command
        curl_command = generate_curl("POST", f"{self.get_vehicle_url}{vehicle_id}", headers)
        logging.info(f"Generated cURL command: {curl_command}")
        print(f"Generated cURL: {curl_command}")

        try:
            response = self.client.get(f"{self.get_vehicle_url}{vehicle_id}", headers=headers)
            if response.status_code == 200:
                vehicle_number = response.json().get("data",{}).get("properties",{}).get("registrationNumber")
                logging.info("Get vehicle number successful: %s", vehicle_number)
                logging.info(response.json())
                return vehicle_number
            else:
                logging.error("Error in vehicle number. Status Code: %s, Response: %s", response.status_code, response.text)
                print(f"Error in getting vehicle number: {response.status_code}, Response: {response.text}")

        except self.client.RequestException as e:
            logging.exception("Error occurred while making vehicle number request: %s", str(e))