import json
import time

import requests
import logging

from locust import HttpUser
from utils.config_loader import CONFIG
from utils.helpers import generate_curl
from utils.file_writer import append_to_json
from apis.get_vehicle_number import GetVehicleNumberModule

# Configure logging
logging.basicConfig(
    filename="attendance.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



class InsertTrackTracesModule(HttpUser):
    def __init__(self,client):
        base_url = CONFIG["base_url_primary"]
        self.create_track_url = base_url + CONFIG["create_track_endpoint"]
        self.client = client
        self.insert_traces_url = base_url + CONFIG["insert_traces_endpoint"]
        self.get_vehicle_number_module = GetVehicleNumberModule(self.client)
        

    def insert_traces(self,token, track_id, rider_id,lat,long):
        if not token:
            logging.error("Error: No authentication token provided. Tracking request aborted.")
            print("Error: No authentication token provided. Tracking request aborted.")
            return

        headers = {
                "X-COREOS-ACCESS": token,
                "Content-Type": "application/json"
            }

        payload = {
                "locationData": [
                    {
                        "app": "",
                        "id": [
                            rider_id
                        ],
                        "md": "REST",
                        "seq": 1015,
                        "tis": 1739254763000,
                        "accuracy": 1.8,
                        "distance": 0.0,
                        "isMobile": True,
                        "lat": lat,
                        "lon": long,
                        "provider": "fused",
                        "speed": 0.0
                    }
                ]
            }
        # Log the generated cURL command
        curl_command = generate_curl("POST", f"{self.insert_traces_url}{track_id}/traces", headers, payload)
        logging.info(f"Generated cURL command: {curl_command}")
        print(f"Generated cURL: {curl_command}")

        try:

            response = self.client.post(f"{self.insert_traces_url}{track_id}/traces", headers=headers, json=payload)

            if response.status_code == 200:
                logging.info("Smartphone tracing inserted successful: %s", response.json())
                append_to_json("track_traces_mapping", track_id, f"Traces Pushed: Lat-{lat} Long-{long} Rider-{rider_id}")
                print("Smartphone tracing inserted successful:", response.json())
            else:
                logging.error("Error in smartphone tracing inserted. Status Code: %s, Response: %s", response.status_code, response.text)
                print(f"Error in smartphone tracing inserted: {response.status_code}, Response: {response.text}")

        except self.client.RequestException as e:
            logging.exception("Error occurred while making tracing inserted request: %s", str(e))
            print("Error: Unable to tracing inserted smartphone. Please check logs for details.")


            

    def create_track(self, token, rider_id, vehicle_id,lat,long):
        if not token:
            logging.error("Error: No authentication token provided. Tracking request aborted.")
            print("Error: No authentication token provided. Tracking request aborted.")
            return

        headers = {
            "X-COREOS-ACCESS": token,
            "Content-Type": "application/json"
        }

        vehicle_number=self.get_vehicle_number_module.get_vehicle_number(token,vehicle_id)
        


        payload = {
            "user_id": rider_id,
            "vehicle_number": vehicle_number
        }

        # Log the generated cURL command
        curl_command = generate_curl("POST", self.create_track_url, headers, payload)
        logging.info(f"Generated cURL command: {curl_command}")
        print(f"Generated cURL: {curl_command}")

        try:
            
            response = self.client.post(self.create_track_url, headers=headers, json=payload)

            if response.status_code == 200:
                logging.info("Smartphone tracking successful: %s", response.json())
                track_id = response.json().get("data",{}).get("track_id")
                time.sleep(5)
                self.insert_traces(token,track_id,rider_id,lat,long)
                print("Smartphone tracking successful:", response.json())
            else:
                logging.error("Error in smartphone tracking. Status Code: %s, Response: %s", response.status_code, response.text)
                print(f"Error in smartphone tracking: {response.status_code}, Response: {response.text}")

        except self.client.RequestException as e:
            logging.exception("Error occurred while making tracking request: %s", str(e))
            print("Error: Unable to track smartphone. Please check logs for details.")


            