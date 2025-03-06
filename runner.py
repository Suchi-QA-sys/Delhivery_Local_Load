from apis.auth_token import AuthModule
from apis.attendance import AttendanceModule
from apis.create_driver import CreateDriverModule
from apis.create_vehicle import CreateVehicleModule
from apis.create_order import CreateOrderModule
from apis.rider_token import RiderAuthModule

class Runner:
    def __init__(self, user):
        self.client = user.client
        self.auth_module = AuthModule(self.client)  
        self.rider_auth_module = RiderAuthModule(self.client)
        self.attendance_module = AttendanceModule(self.client)  
        self.create_driver_module = CreateDriverModule(self.client,)
        self.create_vehicle_module = CreateVehicleModule(self.client)
        self.create_order_module = CreateOrderModule(self.client)
        self.token = None  

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
            print(f"Rider Token fetched successfully: {self.token}")

    def run_attendance(self):
        if not self.token:
            print("No token available. Skipping attendance marking.")
            return
        self.attendance_module.mark_attendance(self.token)

    def run_create_driver(self):
        if not self.token:
            print("No token available. Skipping driver creation.")
            return
        self.create_driver_module.create_driver(self.rider_token)

    def run_create_vehicle(self):
        if not self.token:
            print("No token available. Skipping driver creation.")
            return
        self.create_vehicle_module.create_vehicle(self.token)

    def run_create_order(self):
        if not self.token:
            print("No token available. Skipping driver creation.")
            return
        self.create_order_module.create_order(self.token)