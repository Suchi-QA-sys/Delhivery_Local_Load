from locust import HttpUser, task, between
from runner import Runner

class LoadTest(HttpUser):
    wait_time = between(1, 3)  # Wait time between requests

    def on_start(self):
        self.runner = Runner(self)  # Initialize Runner
        self.runner.setup_auth()  # Fetch auth token first

    @task
    def create_driver(self):
        self.runner.run_create_driver()

    @task
    def mark_attendance(self):
        self.runner.run_attendance()
