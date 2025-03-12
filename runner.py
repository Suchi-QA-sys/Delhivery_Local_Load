from apis.auth_token import AuthModule
from apis.attendance import AttendanceModule
from apis.create_driver import CreateDriverModule
from apis.create_vehicle import CreateVehicleModule
from apis.create_order import CreateOrderModule
from apis.rider_token import RiderAuthModule
from apis.vehicle_token import VehicleAuthModule
from apis.insert_track_traces import InsertTrackTracesModule
from apis.get_allocation_id import GetAllocationIDModule
from apis.get_broadcast_id import GetBroadcastIDModule
from apis.broadcast_action import BroadCastActionModule
from utils.file_reader import get_json_entries_based_on_index
from utils.config_loader import CONFIG
import urllib.parse

class Runner:
    def __init__(self, user):
        self.riders_vehicles = None
        self.client = user.client
        self.auth_module = AuthModule(self.client)
        self.rider_auth_module = RiderAuthModule(self.client)
        self.vehicle_auth_module = VehicleAuthModule(self.client)
        self.attendance_module = AttendanceModule(self.client)
        self.create_driver_module = CreateDriverModule(self.client)
        self.create_vehicle_module = CreateVehicleModule(self.client)
        self.create_order_module = CreateOrderModule(self.client)
        self.insert_track_traces_module = InsertTrackTracesModule(self.client)
        self.get_allocation_id_module = GetAllocationIDModule(self.client)
        self.get_broadcast_id_module = GetBroadcastIDModule(self.client)
        self.broadcast_action_module = BroadCastActionModule(self.client)
        self.token = None
        self.base_rider_vehicles_combination = CONFIG["base_riders_vehicles"]

    def setup_auth(self):
        self.token = self.auth_module.get_auth_token()
        if not self.token:
            print("Authentication failed. No token received.")
        else:
            print(f"Token fetched successfully: {self.token}")

        self.rider_token = self.rider_auth_module.get_rider_token()
        if not self.rider_token:
            print("Authentication failed. No Rider token received.")
        else:
            print(f"Rider Token fetched successfully: {self.rider_token}")

        self.vehicle_token = self.vehicle_auth_module.get_vehicle_token()
        if not self.vehicle_token:
            print("Authentication failed. No Vehicle token received.")
        else:
            print(f"Vehicle Token fetched successfully: {self.vehicle_token}")

    def run_attendance(self, index,action):
        if not self.token:
            print("No token available. Skipping attendance marking.")
            return
        self.riders_vehicles = get_json_entries_based_on_index("rider_vehicle_mapping", index)
        self.attendance_module.mark_attendance(self.token, self.riders_vehicles[0], self.riders_vehicles[1], 23.040233, 72.566623,action)

    def run_create_driver(self):
        if not self.token:
            print("No token available. Skipping driver creation.")
            return
        self.create_driver_module.create_driver(self.rider_token)

    def run_create_vehicle(self):
        if not self.token:
            print("No token available. Skipping vehicle creation.")
            return
        self.create_vehicle_module.create_vehicle(self.vehicle_token)

    def run_create_order(self):
        if not self.token:
            print("No token available. Skipping order creation.")
            return
        job_id = self.create_order_module.create_order(self.token)
        return job_id

    def run_insert_traces(self, index, lat, long):
        if not self.token:
            print("No token available. Skipping trace insertion.")
            return
        self.riders_vehicles = get_json_entries_based_on_index("rider_vehicle_mapping", index)
        self.insert_track_traces_module.create_track(self.token, self.riders_vehicles[0], self.riders_vehicles[1], lat, long)

    def run_get_allocation_id(self, job_id):
        if not self.token:
            print("No token available. Skipping allocation ID retrieval.")
            return
        allocation_id = self.get_allocation_id_module.get_allocation_lists(self.token, job_id)
        return allocation_id

    def run_get_broadcast_id(self, allocation_id):
        if not self.token:
            print("No token available. Skipping broadcast ID retrieval.")
            return
        broadcast_id = self.get_broadcast_id_module.get_broadcast_lists(self.token, allocation_id)
        return broadcast_id

    def run_broadcast_action(self, allocation_id, broadcast_id, rider_id):
        if not self.token:
            print("No token available. Skipping broadcast ID retrieval.")
            return
        broadcast_id = self.broadcast_action_module.punch_broadcast_action(self.token, allocation_id,broadcast_id,rider_id)
        return broadcast_id
