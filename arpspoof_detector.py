import scapy.all as scapy

def get_target_mac(ip_address):
    """Retrieve the MAC address associated with the given IP address."""
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def sniff_traffic(interface):
    """Sniff traffic on the specified network interface."""
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    """Process sniffed packets and detect ARP spoofing attacks."""
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_target_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc

            if real_mac != response_mac:
                print("[+] Network attack detected")
        except IndexError:
            pass

# Specify the network interface to sniff traffic on
sniff_traffic("eth0")

