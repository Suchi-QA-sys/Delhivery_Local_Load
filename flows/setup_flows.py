import logging
import time

from utils.config_loader import CONFIG
from utils.helpers import delete_all_files_of_directory

logger = logging.getLogger(__name__)

def setup_initial_data(runner):
    base_rider_vehicles_combination = CONFIG["base_riders_vehicles"]
    base_order_combination = CONFIG["base_orders"]

    delete_all_files_of_directory("data")


    for i in range(base_rider_vehicles_combination):
        runner.run_create_driver()
        
    for i in range(base_rider_vehicles_combination):
        runner.run_create_vehicle()
        
    for i in range(base_rider_vehicles_combination):
        runner.run_attendance(i,"punch_out")
        runner.run_attendance(i,"punch_in")

    
    for i in range(base_order_combination):
        runner.run_create_order()
        time.sleep(10)



    logger.info("Initial setup complete! Load testing will now begin.")
