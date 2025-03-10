import logging
from utils.config_loader import CONFIG

logger = logging.getLogger(__name__)

def setup_initial_data(runner):
    base_rider_vehicles_combination = CONFIG["base_riders_vehicles"]
    

    for i in range(base_rider_vehicles_combination):
        runner.run_create_driver()
        
    for i in range(base_rider_vehicles_combination):
        runner.run_create_vehicle()

    
    for i in range(base_rider_vehicles_combination):
        runner.run_attendance(i)

    logger.info("Initial setup complete! Load testing will now begin.")
