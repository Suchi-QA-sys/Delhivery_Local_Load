from locust import HttpUser, task, between, tag
from runner import Runner
from utils.config_loader import CONFIG

class LoadTest(HttpUser):
    wait_time = between(1, 3)  # Wait time between requests
    ENABLED_TAGS = CONFIG["enabled_tags"]

    def on_start(self):
        self.runner = Runner(self)  # Initialize Runner
        self.runner.setup_auth()  # Fetch auth token first

    @task
    @tag("driver")
    def create_driver(self):
        if "driver" in ENABLED_TAGS:
            self.runner.run_create_driver()

    @task
    @tag("attendance")
    def mark_attendance(self):
        self.runner.run_attendance()
