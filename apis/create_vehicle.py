import logging
from locust import HttpUser, between
import json
from utils.config_loader import CONFIG
from utils.helpers import generate_curl
from utils.file_reader import get_latest_entry_with_value
from utils.file_writer import update_json_value

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CreateVehicleModule(HttpUser):
    wait_time = between(1, 2)

    def __init__(self, client):
        base_url = CONFIG["base_url_primary"]
        self.create_vehicle_url = base_url + CONFIG["create_vehicle_endpoint"]
        self.client = client
        self.teamid = CONFIG["teams"]["team_id"]
        self.tID = CONFIG["rider"]["x_coreos_tid"]
        self.rider_id = get_latest_entry_with_value("driver_created.json","Synced")

    def create_vehicle(self, token):
        if not token:
            logger.error("Error: No authentication token provided. Vehicle creation aborted.")
            return

        headers = {
            "x-coreos-access": f"{token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-coreos-request-id": "OS1-RequestId:-81bfd767-6647-4632-86f7-6362724fd626",
            "x-coreos-tid":self.tID,
            "x-coreos-userinfo":json.dumps({"id":"07fa25fb-822a-4a87-9920-10ae54125622","name":"Ishan Jain"}),
        }
        payload = {
            "registrationNumber": "38398293",
            "fuelType": "Diesel",
            "vehicleMode": "Road",
            "ownershipType": "Tenant",
            "driverID": self.rider_id,
            "teams": [
                self.teamid
            ],
            "payload": 1000,
            "payloadVolumetric": 1500000,
            "vehicleCategory": "LCV",
            "vehicleSubCategory": "Auto Truck__Diesel__",
            "modelName": "Ape Xtra LDX",
            "referenceNumber": "38398293"
        }

        curl_command = generate_curl("POST", self.create_vehicle_url, headers, payload)
        logger.info(f"Executing: {curl_command}")

        response = self.client.post(self.create_vehicle_url, json=payload, headers=headers)

        if response.status_code == 202:
            update_json_value("driver_created",self.rider_id,"Synced")
            logger.info("Vehicle created successfully.")
        else:
            logger.error(f"Vehicle creation failed: {response.status_code}, Response: {response.text}")
