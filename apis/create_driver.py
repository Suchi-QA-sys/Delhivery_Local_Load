import logging
from locust import HttpUser, between
from utils.config_loader import CONFIG
from utils.helpers import generate_curl,generate_13_digit_number
from utils.file_writer import append_to_json
import json


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CreateDriverModule(HttpUser):
    wait_time = between(1, 2)  # Adjust wait time as needed


    def __init__(self,client):
        base_url = CONFIG["base_url_sandbox"]
        self.create_driver_url = base_url + CONFIG["create_driver_endpoint"]
        self.client = client
        self.teamid = CONFIG["teams"]["team_id"]
        self.tID = CONFIG["rider"]["x_coreos_tid"]
        
    


    def create_driver(self,token):

        if not token:
            logging.error("Error: No authentication token provided. Attendance request aborted.")
            print("Error: No authentication token provided. Attendance request aborted.")
            return

        headers = {
            "x-coreos-access": f"{token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-coreos-request-id": "b26af3a5a1914c158ce4db5a1b81ec59",
            "x-coreos-tid":"delvjkninl",
            "x-coreos-userinfo":json.dumps({"name":"IshanJain","id":"07fa25fb-822a-4a87-9920-10ae54125622"}),
        }


        random_number = generate_13_digit_number()
        random_usercode = generate_13_digit_number()
        payload = {
            "firstName": "test rider",
            "lastName": random_number,
            "primaryMobile": {
                "countryCode": "+91",
                "number": random_number
            },
            "teams": [
                self.teamid
            ],
            "employmentType": "Full-time",
            "designation": "Field Executive",
            "category": "Adhoc",
            "userCode": random_usercode+"script"
        }

        curl_command = generate_curl("POST", self.create_driver_url, headers, payload)
        logger.info(f"Executing: {curl_command}")

        response = self.client.post(self.create_driver_url, json=payload, headers=headers)

        if response.status_code == 202:
            driver_id = response.json().get("data",{}).get("id",{})
            append_to_json("rider_vehicle_mapping", driver_id, "Not Synced")
            logger.info("Driver created successfully.")
        else:
            logger.error(f"Driver creation failed: {response.status_code}, Response: {response.text}")
