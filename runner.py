from apis.auth_token import AuthModule
from apis.attendance import AttendanceModule
from apis.create_driver import CreateDriverModule
from apis.create_vehicle import CreateVehicleModule
from apis.create_order import CreateOrderModule
from apis.rider_token import RiderAuthModule
from apis.vehicle_token import VehicleAuthModule
from apis.insert_track_traces import InsertTrackTracesModule
from utils.file_reader import get_json_entries_based_on_index
from utils.config_loader import CONFIG

class Runner:
    def __init__(self, user):
        self.riders_vehicles = None
        self.client = user.client
        self.auth_module = AuthModule(self.client)  
        self.rider_auth_module = RiderAuthModule(self.client)
        self.vehicle_auth_module = VehicleAuthModule(self.client)
        self.attendance_module = AttendanceModule(self.client)  
        self.create_driver_module = CreateDriverModule(self.client,)
        self.create_vehicle_module = CreateVehicleModule(self.client)
        self.create_order_module = CreateOrderModule(self.client)
        self.insert_track_traces_module = InsertTrackTracesModule(self.client)
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
            print("Authentication failed. No Rider token received.")
        else:
            print(f"Rider Token fetched successfully: {self.vehicle_token}")
            
    def run_attendance(self,index):
        if not self.token:
            print("No token available. Skipping attendance marking.")
            return
        self.riders_vehicles = get_json_entries_based_on_index("rider_vehicle_mapping",index)
        self.attendance_module.mark_attendance(self.token,self.riders_vehicles[0],self.riders_vehicles[1],23.040233,72.566623)

    def run_create_driver(self):
        if not self.token:
            print("No token available. Skipping driver creation.")
            return
        self.create_driver_module.create_driver(self.rider_token)

    def run_create_vehicle(self):
        if not self.token:
            print("No token available. Skipping driver creation.")
            return
        self.create_vehicle_module.create_vehicle(self.vehicle_token)

    def run_create_order(self):
        if not self.token:
            print("No token available. Skipping driver creation.")
            return
        self.create_order_module.create_order(self.token)

    def run_insert_traces(self,index):
        if not self.token:
            print("No token available. Skipping driver creation.")
            return
        self.riders_vehicles  = get_json_entries_based_on_index("rider_vehicle_mapping",index)
        self.insert_track_traces_module.create_track(self.token,self.riders_vehicles[0],self.riders_vehicles[1])