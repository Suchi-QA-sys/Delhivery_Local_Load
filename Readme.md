# Locust Performance Testing Framework

## Overview
This project is a Locust-based performance testing framework designed to evaluate API performance across multiple modules. The framework supports modular API execution based on tags, logging, and automatic cURL command generation for debugging.

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Logging & Debugging](#logging--debugging)

---

## Setup Instructions

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- `pip` package manager
- `virtualenv` (optional but recommended)

### Installation Steps
1. Clone the repository:
   ```sh
   git clone git@github.com:Suchi-QA-sys/Delhivery_Local_Load.git
   cd Delhivery_Local_Load
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source .venv/bin/activate  # It's based on Linux
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

---

## Configuration
All configurations are managed in `base_config.yaml`:

```json
{
  base_url_primary: "https://delvjkninl.sandbox.getos1.com/",
  enabled_tags: ["auth"],
  attendance_endpoint: "local/api/v1/drivers/attendance",
  auth_endpoint: "/core/api/v1/aaa/auth/client-credentials",
  create_driver_endpoint: "/app/api/v2/users",
}
```

## Running Tests

### Running Locust in UI Mode
Start Locust in UI mode using:
```sh
locust
```
Then open `http://localhost:8089` in your browser to configure and start tests.

### Running Locust in Headless Mode
To execute tests in CLI mode, use:
```sh
locust --headless -u 10 -r 2 -t 5m --tags create_driver
```
Where:
- `-u 10` → 10 users (simulated clients)
- `-r 2` → 2 users spawned per second
- `-t 5m` → Run test for 5 minutes
- `--tags create_driver` → Run only `create_driver` tests

---

## Logging & Debugging
- Logs are stored in `logs/locust.log`
- Each API request logs the corresponding cURL command for debugging.
- To enable debug logging, modify `logging.basicConfig(level=logging.DEBUG)` in `utils/logger.py`
