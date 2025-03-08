import logging
import json
import time

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
        secondary_base_url = CONFIG["base_url_primary"]
        self.create_order_url = base_url + CONFIG["create_order_endpoint"]
        self.get_order_id = secondary_base_url + CONFIG["get_order_id_endpoint"]
        self.client = client
        self.teamid = CONFIG["teams"]["team_id"]

    def get_main_order_id(self,od_id):
        token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJLSWo2OFA0STMwZHFSR2pudmtXdmE2WFluMGY2WldlUmlNdC01OUdpMWRJIn0.eyJleHAiOjE3NDE0MTU4NjgsImlhdCI6MTc0MTM0MDQ4NCwiYXV0aF90aW1lIjoxNzQxMzI5NDY4LCJqdGkiOiI4N2RiYTM4Ni04MjFhLTQyZGItOWRhZS0xY2M2NDNkNzU2NjEiLCJpc3MiOiJodHRwczovL2F1dGgtc2IxLnNhbmRib3guZ2V0b3MxLmNvbS9hdXRoL3JlYWxtcy9kZWx2amtuaW5sIiwiYXVkIjpbInBsYXRmb3JtOmFwcDpzZXJ2aWNlOjEwMTJjZWQ0LWQ5MGYtNTAyMi05NTNlLWY4OGVhMjU2M2RmNiIsInBsYXRmb3JtOmFwcDpzZXJ2aWNlOmEyZDA2Y2VhLTZhZjYtNWNkNS05ZTVlLWE1ZGUzZTMxOGY0OCIsInBsYXRmb3JtOmFwcDpvcmRlci1mcGEtd3JhcHBlci1hcGkiLCJwbGF0Zm9ybTphcHA6bG9naXN0aWNzb3JkZXJzZnBhLWJhY2tlbmQiLCJtdGZaclBjeENLNnM0QTN6eFAzeHhEVnN0Vk5LdjhtVyIsInBsYXRmb3JtOmFwcDpidXNpbmVzcy1jb25mLWZwYS1hcGkiLCJwbGF0Zm9ybTphcHA6c2VydmljZTo4YTU5MTdkMy1lZGZlLTVjNWYtODY3MC1lMGUwOGNlZWUwYjUiLCJ5UDlPM1lyWnhuZ3dBM1JCcWZNM1BlQW1acEw0eTFneSIsInBsYXRmb3JtOmFwcDpzZXJ2aWNlOmU3NmUxYTJjLTJjZmMtNTMxNy1hNjI0LWM2MzRhNzhlZjM2ZSIsInBsYXRmb3JtOmFwcDpnZW5pbiIsInBsYXRmb3JtOmFwcDpub3RpZmljYXRpb24tYnVpbGRlciIsIm9TTzhhck1QTWRneXl1Sk12c3ZpQVpJTEtuYmhYWmZkIiwicGxhdGZvcm06YXBwOnNlcnZpY2U6ZTYxOGZhNWEtMDExYy01OTc1LWEwNTktZjU2NjcyYjAxYmJlIiwicGxhdGZvcm06YXBwOnNlcnZpY2U6MTc3NjdiZTMtMzg2OC01MmMyLThkNzUtNjc5M2ZjN2FkM2Y3IiwicGxhdGZvcm06YXBwOmtvbm9oYSIsInBsYXRmb3JtOmFwcDpub3RpZmljYXRpb24tc2VydmljZSIsInBsYXRmb3JtOmFwcDpzZXJ2aWNlOmViNThhOGU5LTA2YmItNTAxOS1hYTRmLTdkODg1MmMxZjEwNSIsIlE5dnJ6U3dXYkp4N2czRUJCTDJVT2FIMkpCTXJHc3hHIl0sInN1YiI6IjYzMjM3YWI5LTlkMjQtNDY0MS1iM2NiLTI0MTkwZDBhNjA2ZiIsInR5cCI6IkJlYXJlciIsImF6cCI6InBsYXRmb3JtOmFwcDpjbGllbnQ6NTllMGM2NDQtNGY4Ny01YTQ3LWFlY2UtOWE0NDJhZjdjY2FkIiwic2Vzc2lvbl9zdGF0ZSI6ImM5NTZjNTUzLWM0NmUtNDhlYi04ZmYyLTRhOWUxODJjZTMzOSIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9kZWx2amtuaW5sLWNkZXYuc2FuZGJveC5nZXRvczEuY29tIiwiaHR0cHM6Ly9kZWx2amtuaW5sLnNhbmRib3guZ2V0b3MxLmNvbSIsImh0dHBzOi8vbG9jYWwuc2FuZGJveC5nZXRvczEuY29tIiwiaHR0cHM6Ly9oeXBlcmxvY2FsZGV2LnNhbmRib3guZ2V0b3MxLmNvbSJdLCJyZXNvdXJjZV9hY2Nlc3MiOnsicGxhdGZvcm06YXBwOnNlcnZpY2U6MTAxMmNlZDQtZDkwZi01MDIyLTk1M2UtZjg4ZWEyNTYzZGY2Ijp7InJvbGVzIjpbIlJvbGU6YW5hbHl0aWNzLWZwYTphbmFseXRpY3MtZnBhLXZpZXdlciJdfSwicGxhdGZvcm06YXBwOnNlcnZpY2U6YTJkMDZjZWEtNmFmNi01Y2Q1LTllNWUtYTVkZTNlMzE4ZjQ4Ijp7InJvbGVzIjpbIlJvbGU6YnVsay11cGxvYWQtdjItZnBhOmJ1bGstdXBsb2FkLWFkbWluIl19LCJwbGF0Zm9ybTphcHA6b3JkZXItZnBhLXdyYXBwZXItYXBpIjp7InJvbGVzIjpbIlJvbGU6b3JkZXItZnBhLXdyYXBwZXItYXBpOmFkbWluLXJvbGUiXX0sInBsYXRmb3JtOmFwcDpsb2dpc3RpY3NvcmRlcnNmcGEtYmFja2VuZCI6eyJyb2xlcyI6WyJSb2xlOmxvZ2lzdGljcy1vcmRlcnMtZnBhOm9yZGVyLWZwYS1hZG1pbiJdfSwibXRmWnJQY3hDSzZzNEEzenhQM3h4RFZzdFZOS3Y4bVciOnsicm9sZXMiOlsiUm9sZTpwYXJ0aWNpcGFudC1mcGE6cGFydGljaXBhbnQtZnBhLWFkbWluIl19LCJwbGF0Zm9ybTphcHA6YnVzaW5lc3MtY29uZi1mcGEtYXBpIjp7InJvbGVzIjpbIlJvbGU6YnVzaW5lc3MtY29uZi1mcGEtYXBpOkJ1c2luZXNzLUNvbmYtQ3JlYXRvci1WaWV3ZXIiXX0sInBsYXRmb3JtOmFwcDpzZXJ2aWNlOjhhNTkxN2QzLWVkZmUtNWM1Zi04NjcwLWUwZTA4Y2VlZTBiNSI6eyJyb2xlcyI6WyJSb2xlOmV0YS10cmFja2luZzp1c2VyLWNvbnRhY3QtcmVhZCIsIlJvbGU6ZXRhLXRyYWNraW5nOmxvY2F0aW9uLXJlYWQiXX0sInlQOU8zWXJaeG5nd0EzUkJxZk0zUGVBbVpwTDR5MWd5Ijp7InJvbGVzIjpbIlJvbGU6c2VydmljZS1vZmZlcmluZy1mcGE6c2VydmljZS1vZmZlcmluZy1mcGEtYWRtaW4iXX0sInBsYXRmb3JtOmFwcDpzZXJ2aWNlOmU3NmUxYTJjLTJjZmMtNTMxNy1hNjI0LWM2MzRhNzhlZjM2ZSI6eyJyb2xlcyI6WyJSb2xlOmh5cGVybG9jYWwtYWxsb2NhdGlvbjpsb2NhbC1hbGxvY2F0ZS1hZG1pbiJdfSwicGxhdGZvcm06YXBwOmdlbmluIjp7InJvbGVzIjpbIlJvbGU6dGhpcmQtcGFydHktcGx1Z2lucy1mcGE6Z2VuaW4tdXNlciJdfSwicGxhdGZvcm06YXBwOm5vdGlmaWNhdGlvbi1idWlsZGVyIjp7InJvbGVzIjpbIlJvbGU6bm90aWZpY2F0aW9uLWJ1aWxkZXItZnBhOmFkbWluLXJvbGUiXX0sIm9TTzhhck1QTWRneXl1Sk12c3ZpQVpJTEtuYmhYWmZkIjp7InJvbGVzIjpbIlJvbGU6ZGlzcGF0Y2gtZnBhOmFkbWluLXJvbGUiXX0sInBsYXRmb3JtOmFwcDpzZXJ2aWNlOmU2MThmYTVhLTAxMWMtNTk3NS1hMDU5LWY1NjY3MmIwMWJiZSI6eyJyb2xlcyI6WyJSb2xlOmRsdmxvY2FsLW9yZGVyLWZwYTpvcmRlci1mcGEtYWRtaW4iXX0sInBsYXRmb3JtOmFwcDpzZXJ2aWNlOjE3NzY3YmUzLTM4NjgtNTJjMi04ZDc1LTY3OTNmYzdhZDNmNyI6eyJyb2xlcyI6WyJSb2xlOmZlYXR1cmUtZmxhZy1mcGE6ZmVhdHVyZS1mbGFncy12aWV3ZXIiXX0sInBsYXRmb3JtOmFwcDprb25vaGEiOnsicm9sZXMiOlsiUm9sZTpyYmNyLWZwYTprb25vaGEtdXNlciJdfSwicGxhdGZvcm06YXBwOm5vdGlmaWNhdGlvbi1zZXJ2aWNlIjp7InJvbGVzIjpbIlJvbGU6bm90aWZpY2F0aW9uLXNlcnZpY2UtZnBhOmFkbWluLXJvbGUiXX0sInBsYXRmb3JtOmFwcDpzZXJ2aWNlOmViNThhOGU5LTA2YmItNTAxOS1hYTRmLTdkODg1MmMxZjEwNSI6eyJyb2xlcyI6WyJSb2xlOnBsYXRmb3JtLXNvbHV0aW9ucy1jb250YWluZXItaGlzdG9yeTpjb250YWluZXItaGlzdG9yeS11c2VyIl19LCJROXZyelN3V2JKeDdnM0VCQkwyVU9hSDJKQk1yR3N4RyI6eyJyb2xlcyI6WyJSb2xlOmNvbnRhaW5lci1mcGEtYXBpOmNvbnRhaW5lci1mcGEtc2hpcG1lbnQtb3BzLXZpZXdlciJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgY29yZW9zIGVtYWlsIiwic2lkIjoiYzk1NmM1NTMtYzQ2ZS00OGViLThmZjItNGE5ZTE4MmNlMzM5IiwidGVuYW50VXVpZCI6InRlbmFudHM6ZTNmNjEyNjUtZDFlMy01ODBhLTkyMGEtMzA5YzZmN2Y3MWY3IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInR6IjoiQXNpYS9Lb2xrYXRhIiwiaHR0cHM6Ly9kZWxoaXZlcnkuY29tL3RlbmFudElkIjoiZGVsdmprbmlubCIsInByZWZlcnJlZF91c2VybmFtZSI6Iis5MTk5ODg3NzY2NTUiLCJnaXZlbl9uYW1lIjoiU2F2ZXJpIiwidXNlcklkIjoiOWQ2OTkxM2QtZmNmNy00YWVjLWE0YTEtY2QyYmNkODgxODMwIiwic2VjdXJpdHlMZXZlbCI6Ik9QRU4iLCJob3N0bmFtZSI6InNhbmRib3guZ2V0b3MxLmNvbSIsImFwcElkIjoicGxhdGZvcm06YXBwOjU5ZTBjNjQ0LTRmODctNWE0Ny1hZWNlLTlhNDQyYWY3Y2NhZC1jbGllbnQiLCJuYW1lIjoiU2F2ZXJpIHN1c2FybGEiLCJ0ZW5hbnRJZCI6ImRlbHZqa25pbmwiLCJodHRwczovL2RlbGhpdmVyeS5jb20vdXNlcklkIjoiOWQ2OTkxM2QtZmNmNy00YWVjLWE0YTEtY2QyYmNkODgxODMwIiwiZmFtaWx5X25hbWUiOiJzdXNhcmxhIiwiZW1haWwiOiJzdXJ5YS5zdXNhcmxhQGRlbGhpdmVyeS5jb20ifQ.eY40Lwty5HC8K27FxcjFZ2EMaHsKAgPDiHkTomYnlJ-uSm9PnlFY6dStF2Lwxvs8dBUn7sbxK5Rl4GfzRYxUWjrV2Spz9ny4qUtnFLQ8n4LsFQLXxQD0ZJl5iqBnFiejSWGZz9me5ejkcov72Ye-TbbI3SkNjjGf7djACBlpqkjR5IAlBl6zUaw0h8ykEMxHdWdQFNjcL8bfHDrNNeJAfTCVqLZO72r4ZUwmhhI43kv6ytXrAKTeAYyXWqSBEQA4QYJPeq9NoKDHarieMPJdA92TGIHEeCKPmX7JoLas-lSMdr1tqDTFBhuMCz_1eoZxARETtjxH_G5OGT_RkgFitg"
        headers = {
            "x-coreos-access": f"{token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-coreos-request-id": "a0ace0f12b5a4b698264e7a85db7bad2",
            "x-coreos-tid":"delvjkninl",
            "x-coreos-userinfo":json.dumps({"name":"Saveri susarla","id":"9d69913d-fcf7-4aec-a4a1-cd2bcd881830"}),
        }
        payload = {
            "offset": 0,
            "size": 10,
            "sort": [
                {
                    "createdAt": {
                        "order": "desc"
                    }
                }
            ],
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "workOrders.attributes.teamId.keyword": self.teamid
                            }
                        },
                        {
                            "bool": {
                                "should": [
                                    {
                                        "bool": {
                                            "must": [
                                                {
                                                    "match": {
                                                        "status.keyword": "inProgress"
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "subStatus.keyword": "scheduled"
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        "bool": {
                                            "must": [
                                                {
                                                    "match": {
                                                        "status.keyword": "inProgress"
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        "subStatus.keyword": "rescheduled"
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    "filter": [
                        {
                            "range": {
                                "workOrders.pickupDetails.nextAttemptPickUpSlot.from": {
                                    "lte": 1741372199999
                                }
                            }
                        }
                    ]
                }
            }
        }

        curl_command = generate_curl("POST", self.get_order_id, headers, payload)
        logger.info(f"Executing: {curl_command}")

        response = self.client.post(self.get_order_id, json=payload, headers=headers)

        if response.status_code == 200:
            logger.info("Got order id api response successfully.")
            main_order_data= response.json().get("data",{})

            for order_details in main_order_data:
                if order_details.get("clientDetails",{}).get("clientOrderId") == od_id:
                    main_order_id = order_details.get("orderId",{})
                    job_id = order_details.get("workOrders")[0].get("attributes",{}).get("jobId")
                    logger.info(f"Main ID and Job ID is {main_order_id} - {job_id}")
                    write_to_file("orders_created", f"{main_order_id} - {od_id} - {job_id},")
            
        else:
            logger.error(f"Order creation failed: {response.status_code}, Response: {response.text}")



    def create_order(self, token):
        if not token:
            logger.error("Error: No authentication token provided. Order creation aborted.")
            return
        
        
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNvdXJjZSI6IldFQiIsInVjaWQiOiJhMDY2Nzk3Mi03YTZhLTA5ODMtNzExOC1lYWIyYjZmMGUzNzgifSwiZXhwIjoxNzQxNDI2ODA1LCJpYXQiOjE3NDEzNDA0MDUsImp0aSI6ImJjZWYzZjQ3LWVhZGYtNDUyYi1hZWM4LWMxODMxYWM3ZDRiYyJ9.oTTfrqLJrUeqBbfqRddS-ri37SYXBgS5GEi1ZNp5Quk"
        headers = {
            "Authorization": f"Bearer {token}",
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
            "vehicle_type": "3-wheeler"
        }

        curl_command = generate_curl("POST", self.create_order_url, headers, payload)
        logger.info(f"Executing: {curl_command}")

        response = self.client.post(self.create_order_url, json=payload, headers=headers)

        if response.status_code == 201:
            logger.info("Order created successfully.")
            client_order_id = response.json().get("data",{}).get("order_id",{})
            time.sleep(6)
            self.get_main_order_id(client_order_id)
        else:
            logger.error(f"Order creation failed: {response.status_code}, Response: {response.text}")

