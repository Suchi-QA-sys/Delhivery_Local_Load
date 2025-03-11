import json
import requests
import logging
from utils.config_loader import CONFIG
from utils.helpers import generate_curl

# Configure logging
logging.basicConfig(
    filename="broadcast_lists.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class GetAllocationID:
    def __init__(self, client):
        base_url = CONFIG["base_url_primary"]
        self.get_allocation_id_url = base_url + CONFIG["get_allocation_id_endpoint"]
        self.client = client

    def get_broadcast_lists(self, token, allocation_id):
        if not token:
            logging.error("Error: No authentication token provided. Broadcast lists request aborted.")
            print("Error: No authentication token provided. Broadcast lists request aborted.")
            return

        headers = {
            "X-COREOS-ACCESS": token,
            "X-COREOS-REQUEST-ID": "rudra-postman",
            "X-COREOS-TID": "delvjkninl",
            "X-COREOS-USERINFO": json.dumps({"user": "rudra", "id": "platform:app:service:86e306d4-564c-5082-90b5-a7ad29fb3579"}),
            "X-COREOS-APPID": "app:45bb8ddb-95d9-5a88-b1ba-2d75fa5ab59e",
            "Content-Type": "application/json"
        }

        query_params = {
            "query": json.dumps({
                "arr": [{
                    "key": "allocationId.keyword",
                    "value": f"allocationJobs:{allocation_id}",
                    "expr": "eq"
                }],
                "op": "and"
            })
        }

        url = f"{self.get_allocation_id_url}"

        # Log the generated cURL command
        curl_command = generate_curl("GET", url, headers, params=query_params)
        logging.info(f"Generated cURL command: {curl_command}")
        print(f"Generated cURL: {curl_command}")

        try:
            response = self.client.get(url, headers=headers, params=query_params)

            if response.status_code == 200:
                logging.info("Broadcast lists retrieved successfully: %s", response.json())
                print("Broadcast lists retrieved successfully:", response.json())
            else:
                logging.error("Error retrieving broadcast lists. Status Code: %s, Response: %s", response.status_code, response.text)
                print(f"Error retrieving broadcast lists: {response.status_code}, Response: {response.text}")

        except requests.RequestException as e:
            logging.exception("Error occurred while making broadcast lists request: %s", str(e))
            print("Error: Unable to retrieve broadcast lists. Please check logs for details.")
