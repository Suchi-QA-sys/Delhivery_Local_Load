import json
import requests
import logging
from utils.config_loader import CONFIG
from utils.helpers import generate_curl

# Configure logging
logging.basicConfig(
    filename="attendance.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class AttendanceModule:
    def __init__(self,client):
        base_url = CONFIG["base_url_primary"]
        self.attendance_url = base_url + CONFIG["attendance_endpoint"]
        self.client = client
        self.last_action = "punch_in"

    def mark_attendance(self, token,riderID, vehicleID, lat, long):
        if not token:
            logging.error("Error: No authentication token provided. Attendance request aborted.")
            print("Error: No authentication token provided. Attendance request aborted.")
            return

        headers = {
            "X-COREOS-TID": "delvjkninl",
            "X-COREOS-REQUEST-ID": "2a2af622-28d7-4d8f-b622-075b2bacb6cf",
            "X-COREOS-USERINFO": json.dumps({"name": "kamalbhayal", "id": "caa4669f-260b-4aab-8892-554ea3ecdf88"}),
            "Content-Type": "application/json"
        }

        if isinstance(token, str) and token.strip():
            headers["X-COREOS-ACCESS"] = token
        else:
            logging.error("Invalid or missing authentication token. Cannot proceed with the request.")
            print("Error: Invalid or missing authentication token. Attendance request aborted.")
            return


        logging.info("Sending attendance marking request to: %s", self.attendance_url)

        # self.last_action = "punch_in" if self.last_action == "punch_out" else "punch_out"

        payload = {
            "userId": riderID,
            "vehicleId": vehicleID,
            "action": self.last_action,
            "lat": lat,
            "long": long
        }

        # Log the generated cURL command
        curl_command = generate_curl("POST", self.attendance_url, headers, payload)
        logging.info(f"Generated cURL command: {curl_command}")
        print(f"Generated cURL: {curl_command}")

        try:
            response = self.client.post(self.attendance_url, headers=headers, json=payload)

            if response.status_code == 200:
                logging.info("Attendance marked successfully: %s", response.json())
                print("Attendance marked successfully:", response.json())
            else:
                logging.error("Error marking attendance. Status Code: %s, Response: %s", response.status_code, response.text)
                print(f"Error marking attendance: {response.status_code}, Response: {response.text}")

        except self.client.RequestException as e:
            logging.exception("Error occurred while making attendance request: %s", str(e))
            print("Error: Unable to mark attendance. Please check logs for details.")
