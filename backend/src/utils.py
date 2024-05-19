import socket

def send_wol(mac_address):
    # Create the magic packet
    if len(mac_address) != 12:
        raise ValueError("Invalid MAC address")
    data = bytes.fromhex('FF' * 6 + mac_address * 16)
    
    # Create a socket to send the packet
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Enable sending of broadcast packets
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Send the magic packet to all devices on the network
        sock.sendto(data, ('255.255.255.255', 9))