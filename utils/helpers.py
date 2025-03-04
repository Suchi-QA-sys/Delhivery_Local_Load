def generate_curl(method, url, headers=None, data=None):
    curl_command = f"curl --location --request {method.upper()} '{url}'"

    if headers:
        for key, value in headers.items():
            curl_command += f" \\\n--header '{key}: {value}'"

    if data:
        curl_command += f" \\\n--data '{data}'"

    print("\nGenerated cURL Command:\n" + curl_command)
    return curl_command
