#!/usr/bin/env python

import requests

# Target URL to send POST request
target_url = "http://.........."
# Dictionary containing login credentials
data_dict = {"username": "admin", "password": "password", "Login": "submit"}

# Send a POST request to the target URL with the provided data dictionary
response = requests.post(target_url, data=data_dict)

# Print the content of the response
print(response.content)

