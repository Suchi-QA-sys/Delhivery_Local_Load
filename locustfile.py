import random

from locust import HttpUser, task, between, tag
from runner import Runner
from utils.config_loader import CONFIG
from flows.setup_flows import setup_initial_data
from flows.setup_broadcast_flows import setup_broadcast_flows
from utils.file_reader import get_json_entries_based_on_index
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
        self.combinations_allocations_broadcasts = []
        self.order_created = False
        self.rider_index = 0
        self.last_broadcast = 0
        

        setup_initial_data(self.runner)

        if "OrderAllocationFlow" in self.ENABLED_TAGS:
            traces_thread = threading.Thread(target=self.create_traces_continuously, daemon=True)
            traces_thread.start()
            logger.info("Started background traces creation thread")

    def create_traces_continuously(self):
        index = 0
    
        while True:
            if index > self.base_rider_vehicles_combination:
                index = 0 
    
            try:
                # Generate a new random index in every iteration
                random_coordinate_index = random.randint(0, 10)
                lat_long_combinations = get_json_entries_based_on_index("lat_long_clusters", random_coordinate_index, "public")
    
                if len(lat_long_combinations) < 2:
                    logger.error("Insufficient data returned from get_json_entries_based_on_index")
                    continue  
    
                
                self.runner.run_insert_traces(index, lat_long_combinations[0], lat_long_combinations[1])
    
                time.sleep(180)
                index += 1
    
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

    @task(2)
    @tag("OrderAllocationFlow")
    def create_order(self):
        if "OrderAllocationFlow" in self.ENABLED_TAGS:
            job_id =self.runner.run_create_order()
            if job_id:
                allocations_broadcasts = setup_broadcast_flows(self.runner,job_id)
                self.combinations_allocations_broadcasts.append(allocations_broadcasts)
                if len(allocations_broadcasts) > 1:
                    self.order_created = True
            else:
                logging.error("No Job ID Found , Allocation and Broadcast call not made")
            
    @task
    @tag("OrderAllocationFlow")
    def create_broadcast_action(self):
        if "OrderAllocationFlow" in self.ENABLED_TAGS and self.order_created:
            if self.rider_index < len(self.base_rider_vehicles_combination):
                rider_vehicle_set = get_json_entries_based_on_index("rider_vehicle_mapping",self.rider_index)
                self.runner.run_broadcast_action(rider_vehicle_set[0],self.combinations_allocations_broadcasts[self.last_broadcast][0],self.combinations_allocations_broadcasts[self.last_broadcast][1])
                self.last_broadcast+=1
                self.rider_index+=1
            else:
                return

