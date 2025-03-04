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
    def __init__(self):
        base_url = CONFIG["base_url_primary"]
        self.attendance_url = base_url + CONFIG["attendance_endpoint"]

    def mark_attendance(self, token):
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
            headers["X-COREOS-ACCESS"] = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJBWnhPMFY4OEVWbkZmSGRsSnltVkJVZDktZFJVY1dsMmxaQ3NCYlZEbmh3In0.eyJleHAiOjE3NDExNzE4NDcsImlhdCI6MTc0MTA4NTQ0NywiYXV0aF90aW1lIjoxNzQxMDg1NDQ3LCJqdGkiOiI3ZjI3ODllMy04NmFmLTQzMmItYjVlZi01YWU3NTNkYzVhMjQiLCJpc3MiOiJodHRwczovL2F1dGguZ2V0b3MxLmNvbS9hdXRoL3JlYWxtcy9kZXZlbG9wZXJwbGF0Zm9ybSIsInN1YiI6IjhmOGUyNzg2LTAyYmMtNDg2Mi04MjMzLTE1N2YyNmY4N2UxYyIsInR5cCI6IkJlYXJlciIsImF6cCI6ImFwcDo6ZGV2ZWxvcGVycGxhdGZvcm0iLCJzZXNzaW9uX3N0YXRlIjoiZTUxODkwYmMtN2YwNi00NDM0LTkyNTUtYWFmNDRhM2FlNjAyIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwic2NvcGUiOiJvcGVuaWQgZGV2ZWxvcGVyX3BvcnRhbF9hdHRyaWJ1dGVfbWFwcGVyIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJlNTE4OTBiYy03ZjA2LTQ0MzQtOTI1NS1hYWY0NGEzYWU2MDIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IlNhdmVyaSBTdXNhcmxhIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic3VyeWEuc3VzYXJsYUBkZWxoaXZlcnkuY29tIiwiZ2l2ZW5fbmFtZSI6IlNhdmVyaSIsImZhbWlseV9uYW1lIjoiU3VzYXJsYSIsInVzZXJJZCI6IjhmOGUyNzg2LTAyYmMtNDg2Mi04MjMzLTE1N2YyNmY4N2UxYyIsImVtYWlsIjoic3VyeWEuc3VzYXJsYUBkZWxoaXZlcnkuY29tIn0.HBtwSqq36SR1udmNCjkxjxMpHvRQ8P73QIyY8EPUkbFWi349IG3AmcNmGoPoa50JJd3j0pAmLZ_AgJAeFkgRlA4wvA2W8wjneOkbXRCElvAb-prUJYrW7dLlosEPy2FrFos85ebkslrrHRmc0iEieNHpRebAYmVAFj1wn3Jlsnoit4LklA3-FFUpBvSqu6QONKgja5VGpYtHUB7_7XkAOkpi7Gvq2BT8UFbk3cgkYC69WtFKiO8jMZB-uhMwg_Ob-ey7c0VJYmju7_mMKYfIaBo07gdY3qabDRG3XhJ0IJCRi2RIW_LH3Orgs8Zi6dTbaA4rSplPZvc19gyken0uKw"
        else:
            logging.error("Invalid or missing authentication token. Cannot proceed with the request.")
            print("Error: Invalid or missing authentication token. Attendance request aborted.")
            return


        logging.info("Sending attendance marking request to: %s", self.attendance_url)

        payload = {
            "userId": "2a2af622-28d7-4d8f-b622-075b2bacb6cf",
            "vehicleId": "vehicles:fa3594cf-b8e1-5aef-889a-25413deec8dd",
            "action": "punch_in",
            "lat": 23.040233,
            "long": 72.566623
        }

        # Log the generated cURL command
        curl_command = generate_curl("POST", self.attendance_url, headers, payload)
        logging.info(f"Generated cURL command: {curl_command}")
        print(f"Generated cURL: {curl_command}")

        try:
            response = requests.post(self.attendance_url, headers=headers, json=payload)

            if response.status_code == 200:
                logging.info("Attendance marked successfully: %s", response.json())
                print("Attendance marked successfully:", response.json())
            else:
                logging.error("Error marking attendance. Status Code: %s, Response: %s", response.status_code, response.text)
                print(f"Error marking attendance: {response.status_code}, Response: {response.text}")

        except requests.RequestException as e:
            logging.exception("Error occurred while making attendance request: %s", str(e))
            print("Error: Unable to mark attendance. Please check logs for details.")
