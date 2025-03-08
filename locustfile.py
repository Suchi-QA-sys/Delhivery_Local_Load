from locust import HttpUser, task, between, tag, run_single_user
from runner import Runner
from utils.config_loader import CONFIG
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class LoadTest(HttpUser):
    wait_time = between(1, 3)  # Wait time between requests


    def on_start(self):
        self.runner = Runner(self) 
        self.runner.setup_auth()  
        self.ENABLED_TAGS = CONFIG["enabled_tags"]
        logger.info(self.ENABLED_TAGS)

    @task
    @tag("driver")
    def create_driver(self):
        if "driver" in self.ENABLED_TAGS:
            self.runner.run_create_driver()

    @task
    @tag("attendance")
    def mark_attendance(self):
        if "attendance" in self.ENABLED_TAGS:
            self.runner.run_attendance()

    @task
    @tag("vehicle")
    def create_vehicle(self):
        if "vehicle" in self.ENABLED_TAGS:
            logger.info("Inside")
            self.runner.run_create_vehicle()

    @task
    @tag("order")
    def create_order(self):
        if "order" in self.ENABLED_TAGS:
            self.runner.run_create_order()
