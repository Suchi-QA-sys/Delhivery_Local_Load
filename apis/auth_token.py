import requests
import logging
from utils.config_loader import CONFIG
from utils.file_writer import write_to_file
from utils.helpers import generate_curl

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AuthModule:
    def __init__(self,client):
        self.auth_url = CONFIG["base_url_primary"] + CONFIG["auth_task_endpoint"]
        self.client = client

    def get_auth_token(self):
        headers = {
            "Content-Type": "application/json",
            "X-COREOS-TID": "delvjkninl",
            "X-COREOS-REQUEST-ID": "unique-request-id"
        }

        payload = {
            "clientId": CONFIG["auth"]["client_id"],
            "clientSecret": CONFIG["auth"]["client_secret"],
            "audience": CONFIG["auth"]["audience"]
        }

        logging.info("Sending authentication request to: %s", self.auth_url)

        try:
            response = self.client.post(self.auth_url, headers=headers, json=payload)
            response_data = response.json()

            curl_command = generate_curl("POST", self.auth_url, headers, payload)
            logger.info(f"Executing: {curl_command}")

            if response.status_code == 200:
                token = response_data.get("data", {}).get("accessToken")
                if token:
                    # Log the token
                    write_to_file("auth_token", f"accessToken: {token}\n")
                    logging.info("Authentication successful. Token received.")
                    return token
                else:
                    logging.error("Error: Token not found in response. Response: %s", response_data)
            else:
                logging.error("Authentication failed. Status Code: %s, Response: %s", response.status_code, response.text)

        except requests.RequestException as e:
            logging.exception("Error occurred while making authentication request: %s", str(e))

        return None
