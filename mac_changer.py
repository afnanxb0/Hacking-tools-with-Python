import subprocess
import optparse
import re

def get_cli_arguments():
    """Parse command line arguments for the interface and new MAC address."""
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Network interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Desired new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")
    return options

def update_mac_address(interface, new_mac):
    """Change the MAC address of the specified network interface."""
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_mac_address(interface):
    """Retrieve the current MAC address of the specified network interface."""
    # Execute ifconfig command and capture its output
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # Extract the MAC address from the output using a regular expression
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[+] Could not find the MAC address.")
        return None

# Parse command line arguments
cli_options = get_cli_arguments()

# Get and display the current MAC address
current_mac_address = get_mac_address(cli_options.interface)
print(f"Current MAC: {current_mac_address}")

# Update the MAC address
update_mac_address(cli_options.interface, cli_options.new_mac)

# Verify and display the updated MAC address
updated_mac_address = get_mac_address(cli_options.interface)
if updated_mac_address == cli_options.new_mac:
    print(f"[+] MAC address was successfully changed to {updated_mac_address}")
else:
    print(f"[-] MAC address did not get changed.")

