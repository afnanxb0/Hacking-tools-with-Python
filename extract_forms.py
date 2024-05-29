#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

# Function to send HTTP GET request
def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

# Target URL to scrape
target_url = "http://.........."
# Send HTTP GET request to the target URL
response = request(target_url)

# Parse the HTML content of the response
parsed_html = BeautifulSoup(response.content, "html.parser")
# Find all form elements in the parsed HTML
forms_list = parsed_html.findAll("form")

# Iterate over each form element
for form in forms_list:
    # Extract form action and method
    action = form.get("action")
    print(action)
    method = form.get("method")
    print(method)

    # Find all input elements within the form
    inputs_list = form.findAll("input")
    post_data = {}
    # Iterate over each input element
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        # If input type is text, set input value to "test"
        if input_type == "text":
            input_value = "test"

        # Add input name and value to the post data dictionary
        post_data[input_name] = input_value
        
    # Send HTTP POST request with form data
    result = requests.post(target_url + action, data=post_data)
    # Print the content of the response
    print(result.content)

