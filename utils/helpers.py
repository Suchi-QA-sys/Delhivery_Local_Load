import time
import random
import os
import json
import shutil
import urllib.parse


def generate_curl(method, url, headers=None, params=None, data=None):
    curl_command = f"curl --location --request {method.upper()} '{url}'"

    if headers:
        for key, value in headers.items():
            curl_command += f" \\\n--header '{key}: {value}'"

    if params:
        curl_command += f" \\\n--get --data-urlencode '{params}'"

    if data:
        import json
        if isinstance(data, dict):
            data = json.dumps(data)
        curl_command += f" \\\n--data '{data}'"

    print("\nGenerated cURL Command:\n" + curl_command)
    return curl_command

def generate_13_digit_number():

    timestamp_ms = int(time.time() * 1000)  # Current timestamp in milliseconds (first 10 digits)
    random_part = random.randint(100, 999)  # Random 3-digit number

    return str(timestamp_ms)[:10] + str(random_part)


def delete_all_files_of_directory(dir_name):
    data_dir = dir_name
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
        print(f"🗑️ Deleted all files in '{data_dir}' directory.")
    else:
        print(f"⚠️ Directory '{data_dir}' does not exist.")

def encode_query_params(query_dict):
    json_str = json.dumps(query_dict, separators=(",", ":"))  # Minified JSON
    return json_str

