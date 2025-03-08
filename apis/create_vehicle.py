import logging
from locust import HttpUser, between
import json
from utils.config_loader import CONFIG
from utils.helpers import generate_curl,generate_13_digit_number
from utils.file_reader import get_latest_entry_with_value
from utils.file_writer import update_json_value

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CreateVehicleModule(HttpUser):
    wait_time = between(1, 2)

    def __init__(self, client):
        logger.info("Inside")
        base_url = CONFIG["base_url_vehicle"]
        self.create_vehicle_url = base_url + CONFIG["create_vehicle_endpoint"]
        self.client = client
        self.teamid = CONFIG["teams"]["team_id"]
        self.tID = CONFIG["rider"]["x_coreos_tid"]
        self.synced_riders = []
        self.rider_id = get_latest_entry_with_value("rider_vehicle_mapping","Not Synced",self.synced_riders)
        self.contract = CONFIG["vehicle"]["contract_type"]
        self.vehicle_category = CONFIG["vehicle"]["vehicle_category"]
        self.vehicle_sub_category = CONFIG["vehicle"]["vehicle_subcategory"]
        self.model = CONFIG["vehicle"]["model"]
        logger.info(self.rider_id)
        self.random_number = generate_13_digit_number()
        self.dist_count = 1

    def create_vehicle(self, token):
        if not token:
            logger.error("Error: No authentication token provided. Vehicle creation aborted.")
            return

        self.rider_id = get_latest_entry_with_value("rider_vehicle_mapping","Not Synced",self.synced_riders)

        headers = {
            "x-coreos-access": f"{token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-coreos-request-id": "OS1-RequestId:-81bfd767-6647-4632-86f7-6362724fd626",
            "x-coreos-tid":self.tID,
            "x-coreos-userinfo":json.dumps({"id":"07fa25fb-822a-4a87-9920-10ae54125622","name":"Ishan Jain"}),
        }
        payload = {
            "registrationNumber": f'{self.random_number}{self.dist_count}',
            "fuelType": "Diesel",
            "vehicleMode": "Road",
            "contractType": self.contract,
            "ownershipType": "Tenant",
            "driverID": self.rider_id,
            "teams": [
                self.teamid
            ],
            "payload": 1000,
            "payloadVolumetric": 1500000,
            "vehicleCategory": self.vehicle_category,
            "vehicleSubCategory": self.vehicle_sub_category,
            "modelName": self.model,
            "referenceNumber": f'{self.random_number}{self.dist_count}'
        }

        curl_command = generate_curl("POST", self.create_vehicle_url, headers, payload)
        logger.info(f"Executing: {curl_command}")

        response = self.client.post(self.create_vehicle_url, json=payload, headers=headers)

        vehicle_id = response.json().get("data",{}).get("id",{})

        if response.status_code == 202:
            update_json_value("rider_vehicle_mapping",self.rider_id,vehicle_id)
            self.dist_count = self.dist_count +1
            self.synced_riders.append(self.rider_id)
            logger.info("Vehicle created successfully.")
        else:
            logger.error(f"Vehicle creation failed: {response.status_code}, Response: {response.text}")
