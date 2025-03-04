import logging
from locust import HttpUser, task, between
import requests
from utils.config_loader import CONFIG
from utils.helpers import generate_curl


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CreateDriverModule(HttpUser):
    wait_time = between(1, 2)  # Adjust wait time as needed


    def __init__(self,client):
        base_url = CONFIG["base_url_primary"]
        self.create_driver_url = base_url + CONFIG["create_driver_endpoint"]
        self.client = client


    def create_driver(self,token):

        if not token:
            logging.error("Error: No authentication token provided. Attendance request aborted.")
            print("Error: No authentication token provided. Attendance request aborted.")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "firstName": "Test",
            "lastName": "Driver",
            "primaryMobile": {"countryCode": "+91", "number": "9876543210"},
            "teams": ["teams:59d75559-a342-58f3-ad9b-c55f1dcc7c24", "teams:3f8a2ef7-148e-5f61-a8a8-59137e701022"],
            "employmentType": "Full-time",
            "designation": "Field Executive",
            "category": "Adhoc"
        }

        curl_command = generate_curl("POST", self.create_driver_url, headers, payload)
        logger.info(f"Executing: {curl_command}")

        response = self.client.post(self.create_driver_url, json=payload, headers=headers)

        if response.status_code == 202:
            logger.info("Driver created successfully.")
        else:
            logger.error(f"Driver creation failed: {response.status_code}, Response: {response.text}")
