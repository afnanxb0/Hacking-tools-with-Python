#!/usr/bin/env python

import requests

def download_file(url):
    """Download a file from the specified URL."""
    response = requests.get(url)
    if response.status_code == 200:
        file_name = url.split("/")[-1]
        with open(file_name, "wb") as output_file:
            output_file.write(response.content)
        print("[+] File downloaded successfully.")
    else:
        print("[-] Failed to download file. HTTP status code:", response.status_code)

# Replace "URL......" with the actual URL you want to download from
download_file("URL......")

