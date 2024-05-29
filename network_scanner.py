import scapy.all as scapy
import argparse

# Function to parse command-line arguments
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    options = parser.parse_args()
    return options

# Function to perform ARP scan
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

# Function to print scan results
def print_result(result_list):
    print("IP\t\t\tMAC Address\n------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])

# Main function
def main():
    options = get_arguments()
    target = options.target
    if not target:
        print("[-] Please specify a target IP / IP range.")
        return
    scan_result = scan(target)
    print_result(scan_result)

# Entry point of the program
if __name__ == "__main__":
    main()

