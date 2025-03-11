import json
import requests
import logging
from utils.config_loader import CONFIG
from utils.helpers import generate_curl
from utils.file_writer import append_to_json

# Configure logging
logging.basicConfig(
    filename="broadcast_lists.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class GetAllocationIDModule:
    def __init__(self, client):
        base_url = CONFIG["base_url_primary"]
        self.get_allocation_id_url = base_url + CONFIG["get_allocation_id_endpoint"]
        self.client = client

    def get_allocation_lists(self, token, job_id):
        if not token:
            logging.error("Error: No authentication token provided. Allocation lists request aborted.")
            print("Error: No authentication token provided. Allocation lists request aborted.")
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
            "query": json.dumps({"arr": [{"key": "jobId.keyword", "value": f"{job_id}", "expr": "eq"}], "op": "and"})
        }

        url = f"{self.get_allocation_id_url}"

        # Log the generated cURL command
        curl_command = generate_curl("GET", url, headers, params=query_params)
        logging.info(f"Generated cURL command: {curl_command}")
        print(f"Generated cURL: {curl_command}")

        try:
            response = self.client.get(url, headers=headers, params=query_params)

            if response.status_code == 200:
                logging.info("Allocation lists retrieved successfully: %s", response.json())
                print("Allocation lists retrieved successfully:", response.json())
                allocation_id = response.json().get("data",{}).get("id",{})
                append_to_json("allocationID_broadcastID_mapping", allocation_id, "Not Mapped")
                return allocation_id
            else:
                logging.error("Error retrieving Allocation lists. Status Code: %s, Response: %s", response.status_code, response.text)
                print(f"Error retrieving Allocation lists: {response.status_code}, Response: {response.text}")

        except requests.RequestException as e:
            logging.exception("Error occurred while making Allocation lists request: %s", str(e))
            print("Error: Unable to retrieve Allocation lists. Please check logs for details.")
