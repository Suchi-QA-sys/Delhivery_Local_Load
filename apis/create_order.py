import logging
from locust import HttpUser, task, between
from utils.config_loader import CONFIG
from utils.helpers import generate_curl

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CreateOrderModule(HttpUser):
    wait_time = between(1, 2)

    def __init__(self, client):
        base_url = CONFIG["base_url_primary"]
        self.create_order_url = base_url + CONFIG["create_order_endpoint"]
        self.client = client

    def create_order(self, token):
        if not token:
            logger.error("Error: No authentication token provided. Order creation aborted.")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "origin": {
                "name": "Kamal",
                "address": "Yeshwanthpur Railway Quarters Block-B7, Yeshwanthpur Railway Quarters, Pampanagar, Yeswanthpur",
                "city": "Bengaluru",
                "state": "karnataka",
                "pincode": "560022",
                "phone": "9945735314",
                "email": "kamalkant.bhayal@delhivery.com",
                "lat": "13.009005901095378",
                "lon": "77.54969855770469"
            },
            "destination": {
                "name": "Kamal",
                "address": "474, 1st Main Rd, MSHC Layout, Anandnagar, Hebbal",
                "city": "Bengaluru",
                "state": "karnataka",
                "pincode": "560024",
                "phone": "9945735314",
                "lat": "13.016951069811588",
                "lon": "77.56709100678563"
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

        if response.status_code == 202:
            logger.info("Order created successfully.")
        else:
            logger.error(f"Order creation failed: {response.status_code}, Response: {response.text}")
