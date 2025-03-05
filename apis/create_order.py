import logging
from locust import HttpUser, task, between
from utils.config_loader import CONFIG
from utils.helpers import generate_curl
from utils.file_writer import write_to_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CreateOrderModule(HttpUser):
    wait_time = between(1, 2)

    def __init__(self, client):
        base_url = CONFIG["base_url_thunderbolt"]
        self.create_order_url = base_url + CONFIG["create_order_endpoint"]
        self.client = client

    def create_order(self, token):
        if not token:
            logger.error("Error: No authentication token provided. Order creation aborted.")
            return
        
        
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNvdXJjZSI6IldFQiIsInVjaWQiOiIxMGFmMmI0NC02ZTE3LTUzOGUtODdhNi0zMTE2NDNjNjMyZTIifSwiZXhwIjoxNzQxMjU0MjY4LCJpYXQiOjE3NDExNjc4NjgsImp0aSI6IjY0NDcyZTMxLWUyYmItNGVhMC05ZTg4LWJmMTYyYTIyYmQ5ZSJ9.9ri0nqOrJQcV-LGtSYySUgrJKdHGNYyj09QIV4l7C_Q"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "origin": {
                "name": "Saveri",
                "address": "BTM 2nd stage",
                "city": "Bengaluru",
                "state": "karnataka",
                "pincode": "560076",
                "phone": "9945735314",
                "email": "surya.susarla@delhivery.com",
                "lat": "12.912898408162409",
                "lon": "77.60145363424905"
            },
            "destination": {
                "name": "Suchintan Das",
                "address": "770, 12th A Main Rd, HAL 2nd Stage, Doopanahalli, Indiranagar",
                "city": "Bengaluru",
                "state": "karnataka",
                "pincode": "560024",
                "phone": "9945735314",
                "lat": "12.970293269103966",
                "lon": "77.64112381174671"
            },
            "package_type": "local",
            "service": "local",
            "description": {
                "category": "goods",
                "subcategory": "local"
            },
            "pickup_date": "1740997173",
            "payment_method": "pay at pickup",
            "vehicle_type": "3-wheeler"
        }

        curl_command = generate_curl("POST", self.create_order_url, headers, payload)
        logger.info(f"Executing: {curl_command}")

        response = self.client.post(self.create_order_url, json=payload, headers=headers)

        if response.status_code == 201:
            logger.info("Order created successfully.")
            order_id = response.json().get("data",{}).get("order_id",{})
            write_to_file("orders_created", f"Order Number: {order_id}\n")
        else:
            logger.error(f"Order creation failed: {response.status_code}, Response: {response.text}")
