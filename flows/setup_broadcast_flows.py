import logging
import time


logger = logging.getLogger(__name__)

def setup_broadcast_flows(runner,job_id):
    
    allocation_id = runner.run_get_allocation_id(job_id)
    broadcast_id = runner.run_get_broadcast_id(allocation_id)
    
    time.sleep(2)
    
    return [allocation_id,broadcast_id]
    