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

        setup_initial_data(self.runner)

        if "OrderAllocationFlow" in self.ENABLED_TAGS:
            order_thread = threading.Thread(target=self.create_orders_continuously, daemon=True)
            order_thread.start()
            logger.info("Started background order creation thread")

    def create_orders_continuously(self):
        while True:
            try:
                self.runner.run_create_order()
                time.sleep(120)
            except Exception as e:
                logger.error(f"Error creating order: {e}")

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

    @task
    @tag("OrderAllocationFlow")
    def order_happy_flow(self):
        if "order_allocation" in self.ENABLED_TAGS:
            self.runner.run_order_happy_flow()
