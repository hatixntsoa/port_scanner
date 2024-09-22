import socket
from threading import Thread, Lock
import time
import argparse

# Lock for thread-safe printing
print_lock = Lock()

# Dictionary of common ports and their service names
service_names = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP Alternative",
}

def get_service_name(port):
    """Return the service name for the given port."""
    return service_names.get(port, "Unknown Service")

def scan_port(ip, port, protocol, timeout):
    """Scan a single port on the given IP address."""
    try:
        if protocol == 'tcp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = get_service_name(port)
                with print_lock:
                    print(f"Port {port} (TCP) is open - {service}")
        elif protocol == 'udp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(b'', (ip, port))  # Send a blank packet
            try:
                sock.recvfrom(1024)  # Wait for a response
                service = get_service_name(port)
                with print_lock:
                    print(f"Port {port} (UDP) is open - {service}")
            except socket.timeout:
                pass  # If no response, treat it as closed for UDP
        sock.close()
    except Exception as e:
        with print_lock:
            print(f"Error scanning port {port}: {e}")

def port_scanner(ip, start_port, end_port, protocol, timeout):
    """Scan a range of ports on the given IP address."""
    threads = []
    for port in range(start_port, end_port + 1):
        thread = Thread(target=scan_port, args=(ip, port, protocol, timeout))
        thread.start()
        threads.append(thread)

        # Optional: Rate limiting
        time.sleep(0.01)  # Pause briefly to avoid overwhelming the target

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def main():
    parser = argparse.ArgumentParser(description="Port Scanner Tool")

    parser.add_argument('-ip', '--ip-address', help="IP address to scan")
    parser.add_argument('-r', '--range', help="Port range to scan (e.g., 80-443)")
    parser.add_argument('-p', '--protocol', choices=['tcp', 'udp'], default='tcp', help="Protocol to use (default: tcp)")
    parser.add_argument('-t', '--timeout', type=float, default=1.0, help="Timeout in seconds (default: 1.0)")

    args = parser.parse_args()

    # Prompt for missing arguments
    if not args.ip_address:
        args.ip_address = input("Enter the IP address to scan: ")

    if not args.range:
        args.range = input("Enter the port range (e.g., 80-443): ")

    start_port, end_port = map(int, args.range.split('-'))

    # If protocol is not provided, default to 'tcp'
    protocol = args.protocol

    # If timeout is not provided, default to 1.0 seconds
    timeout = args.timeout

    print(f"Scanning {args.ip_address} for {protocol.upper()} ports from {start_port} to {end_port}...")
    port_scanner(args.ip_address, start_port, end_port, protocol, timeout)

if __name__ == "__main__":
    main()