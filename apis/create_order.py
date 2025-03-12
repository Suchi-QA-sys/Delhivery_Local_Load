import logging
import json
import time

from locust import HttpUser, task, between
from utils.config_loader import CONFIG
from utils.helpers import generate_curl
from utils.file_writer import append_to_json,update_json_value,write_to_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CreateOrderModule(HttpUser):
    wait_time = between(1, 2)

    def __init__(self, client):
        base_url = CONFIG["base_url_thunderbolt"]
        base_url_primary = CONFIG["base_url_primary"]
        self.create_order_url = base_url + CONFIG["create_order_endpoint"]
        self.get_order_id = base_url_primary + CONFIG["get_order_id_endpoint"]
        self.client = client
        self.teamid = CONFIG["teams"]["team_id"]

    def get_main_order_id(self,od_id,token):
        headers = {
            "x-coreos-access": f"{token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-coreos-request-id": "a0ace0f12b5a4b698264e7a85db7bad2",
            "x-coreos-tid":"delvjkninl",
            "x-coreos-userinfo":json.dumps({"name":"kamalbhayal","id":"caa4669f-260b-4aab-8892-554ea3ecdf88"}),
        }

        curl_command = generate_curl("GET", f"{self.get_order_id}/{od_id}", headers)
        logger.info(f"Executing: {curl_command}")

        response = self.client.get(f"{self.get_order_id}/{od_id}", headers=headers)

        if response.status_code == 200:
            logger.info("Got order id api response successfully.")
            main_order_data= response.json().get("data",{})

            for order_details in main_order_data:
                if order_details.get("clientDetails",{}).get("clientOrderId") == od_id:
                    main_order_id = order_details.get("orderId",{})
                    job_id = order_details.get("workOrders")[0].get("attributes",{}).get("jobId")
                    logger.info(f"Main ID and Job ID is {main_order_id} - {job_id}")
                    time.sleep(3)
                    write_to_file("order_listing_api_response",f"{od_id} - {main_order_data}")
                    append_to_json("order_id_job_id_mapping", main_order_id, job_id)
                    append_to_json("jobID_allocationID_mapping", job_id, "Not Mapped")
                    time.sleep(1)
                    update_json_value("clientNumber_orderID_mapping",od_id,main_order_id)
                    return job_id
            
        else:
            logger.error(f"Order creation failed: {response.status_code}, Response: {response.text}")



    def create_order(self, token):
        if not token:
            logger.error("Error: No authentication token provided. Order creation aborted.")
            return
        hard_coded_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNvdXJjZSI6IldFQiIsInVjaWQiOiJhMDY2Nzk3Mi03YTZhLTA5ODMtNzExOC1lYWIyYjZmMGUzNzgifSwiZXhwIjoxNzQxODUxMTk3LCJpYXQiOjE3NDE3NjQ3OTcsImp0aSI6Ijg0MmQ2N2JjLTY5N2UtNDZjMy1iMDRmLWY3ODkxMWQ5NTRlYiJ9.NuzINWg3CECLDvYJzZnVXb0GFtg_Zrrtxc_gqt4cVso"
        headers = {
            "Authorization": f"Bearer {hard_coded_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "origin": {
                "name": "Saveri",
                "address": "401,Golf Course Road, Suncity, Sector54, ggn8, haryana",
                "city": "Gurgaon",
                "state": "Haryana",
                "pincode": "122003",
                "phone": "9945735314",
                "email": "surya.susarla@delhivery.com",
                "lat": "28.455786623246603",
                "lon": "77.09099946132055"
            },
            "destination": {
                "name": "Suchintan Das",
                "address": "Sector 44, gurgaon, haryana",
                "city": "Gurgaon",
                "state": "Haryana",
                "pincode": "122001",
                "phone": "9945735314",
                "lat": "28.456339944680348",
                "lon": "77.07038267568173"
            },
            "package_type": "local",
            "service": "local",
            "description": {
                "category": "goods",
                "subcategory": "local"
            },
            "pickup_date": "1741149092",
            "payment_method": "pay at delivery",
            "vehicle_type": "2-wheeler"
        }


        curl_command = generate_curl("POST", self.create_order_url, headers, payload)
        logger.info(f"Executing: {curl_command}")

        response = self.client.post(self.create_order_url, json=payload, headers=headers)

        if response.status_code == 201:
            logger.info("Order created successfully.")
            client_order_id = response.json().get("data",{}).get("order_id",{})
            append_to_json("clientNumber_orderID_mapping", client_order_id, "Not Mapped")
            time.sleep(6)
            job_id = self.get_main_order_id(client_order_id,token)
            return job_id
        else:
            logger.error(f"Order creation failed: {response.status_code}, Response: {response.text}")

