from apis.auth import AuthModule
from apis.attendance import AttendanceModule
from apis.create_driver import CreateDriverModule

class Runner:
    def __init__(self, user):
        self.client = user.client  # Use the client's session
        self.auth_module = AuthModule(self.client)  # Pass client
        self.attendance_module = AttendanceModule(self.client)  # Pass client
        self.create_driver_module = CreateDriverModule(self.client)  # Pass client
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
            print("No token available. Skipping driver creation.")
            return
        self.create_driver_module.create_driver(self.token)
