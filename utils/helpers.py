import time
import random 


def generate_curl(method, url, headers=None, data=None):
    curl_command = f"curl --location --request {method.upper()} '{url}'"

    if headers:
        for key, value in headers.items():
            curl_command += f" \\\n--header '{key}: {value}'"

    if data:
        curl_command += f" \\\n--data '{data}'"

    print("\nGenerated cURL Command:\n" + curl_command)
    return curl_command

def generate_13_digit_number():

    timestamp_ms = int(time.time() * 1000)  # Current timestamp in milliseconds (first 10 digits)
    random_part = random.randint(100, 999)  # Random 3-digit number

    return str(timestamp_ms)[:10] + str(random_part)  # Ensures exactly 13 digits
