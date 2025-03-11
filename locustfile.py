from locust import HttpUser, task, between, tag
from runner import Runner
from utils.config_loader import CONFIG
from flows.setup_flows import setup_initial_data
import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class LoadTest(HttpUser):
    wait_time = between(1, 3)
    

    def on_start(self):
        self.runner = Runner(self)
        self.runner.setup_auth()
        self.ENABLED_TAGS = CONFIG["enabled_tags"]
        logger.info(f"Enabled tags: {self.ENABLED_TAGS}")
        self.base_rider_vehicles_combination = CONFIG["base_riders_vehicles"]

        setup_initial_data(self.runner)

        if "OrderAllocationFlow" in self.ENABLED_TAGS:
            traces_thread = threading.Thread(target=self.create_traces_continuously, daemon=True)
            traces_thread.start()
            logger.info("Started background traces creation thread")

    def create_traces_continuously(self):
        index = 0
        while True:
            if index > self.base_rider_vehicles_combination:
                    index=0
            try:
                self.runner.run_insert_traces(index)
                time.sleep(180)
                index=index+1
            except Exception as e:
                logger.error(f"Error creating traces: {e}")
                time.sleep(180)

    @task
    @tag("driver")
    def create_driver(self):
        if "driver" in self.ENABLED_TAGS:
            self.runner.run_create_driver()


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

