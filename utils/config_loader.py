import yaml
import os

# Get the absolute path of the config file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of config_loader.py
CONFIG_PATH = os.path.join(BASE_DIR, "../base_config.yaml")  # Adjust based on actual location

def load_config():
    try:
        with open(CONFIG_PATH, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"⚠️  Config file not found: {CONFIG_PATH}")
        return {}

CONFIG = load_config()
