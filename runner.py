from apis.auth import AuthModule
from apis.attendance import AttendanceModule
from apis.create_driver import CreateDriverModule

class Runner:
    def __init__(self, user):
        self.user = user
        self.auth_module = AuthModule()
        self.attendance_module = AttendanceModule()
        self.create_driver_module = CreateDriverModule()
        self.token = None  # Token will be set after authentication

    def setup_auth(self):
        self.token = self.auth_module.get_auth_token()
        if not self.token:
            print("Authentication failed. No token received.")
        else:
            print(f"Token fetched successfully: {self.token}")

    def run_attendance(self):
        if not self.token:
            print("No token available. Skipping attendance marking.")
            return
        self.attendance_module.mark_attendance(self.token)

    def run_create_driver(self):
        if not self.token:
            print("No token available. Skipping attendance marking.")
            return
        self.create_driver_module.create_driver(self.token)
