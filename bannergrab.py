import socket
import argparse

def banner_grabbing(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        sock.send(b"HEAD / HTTP/1.1\r\n\r\n")
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        return banner.split("\n")[0]
    except Exception as e:
        return ""

def scan_ports(ip, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):  # Scan ports in the specified range
        banner = banner_grabbing(ip, port)
        if banner:
            open_ports.append((port, banner))
    return open_ports

def main():
    parser = argparse.ArgumentParser(description="Extract service and version information from open ports.")
    parser.add_argument("ip", type=str, help="Target IP address")
    parser.add_argument("-s", "--start-port", type=int, default=1, help="Start port for the range (default is 1)")
    parser.add_argument("-e", "--end-port", type=int, default=1024, help="End port for the range (default is 1024)")

    args = parser.parse_args()
    target_ip = args.ip
    start_port = args.start_port
    end_port = args.end_port

    open_ports = scan_ports(target_ip, start_port, end_port)

    if open_ports:
        print(f"{target_ip} Ports open at:")
        for port, banner in open_ports:
            print(f"Port {port}: {banner}")
    else:
        print(f"{target_ip} No open ports found in the specified range.")

if __name__ == "__main__":
    main()
