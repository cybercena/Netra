import scapy.all as scapy
import socket

# Function to get the local IP address
def get_local_ip():
    return scapy.get_if_addr(scapy.conf.iface)

# Function to resolve the hostname from the IP address
def resolve_hostname(ip):
    try:
        # Try reverse DNS lookup
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        # If reverse lookup fails, return the IP address itself
        return ip

# Function to scan the network and get connected devices
def scan_network():
    # Get the local IP address and subnet
    local_ip = get_local_ip()
    subnet = ".".join(local_ip.split('.')[:-1]) + ".0/24"
    
    # Create an ARP request packet
    arp_request = scapy.ARP(pdst=subnet)
    ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether_frame / arp_request

    # Send the packet and receive the response
    try:
        result = scapy.srp(packet, timeout=2, verbose=False)[0]
        devices = []
        
        # Loop through the responses and resolve the hostnames
        for sent, received in result:
            hostname = resolve_hostname(received.psrc)
            devices.append((received.psrc, hostname, received.hwsrc))
        
        return devices
    except PermissionError:
        print("Permission Error: Please run the script with administrator privileges.")
        return []

# Main function to print device details
def main():
    devices = scan_network()
    
    if devices:
        print(f"{'IP Address':<20} {'Hostname':<30} {'MAC Address'}")
        print("="*60)
        
        for device in devices:
            print(f"{device[0]:<20} {device[1]:<30} {device[2]}")
    else:
        print("No devices found or permission error.")

if __name__ == "__main__":
    main()
