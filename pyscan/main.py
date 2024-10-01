import socket
from threading import Thread, Lock
import time
import argparse
from importlib.metadata import version, PackageNotFoundError
from typing import Optional

# Determine if the script is being run as standalone or as a package
is_standalone = __name__ == "__main__"

# Import based on execution context
if is_standalone:
    from service_names import service_names
else:
    from pyscan.service_names import service_names

# Lock for thread-safe printing
print_lock = Lock()

# Hardcoded version when run standalone
__version__ = "0.1.1"


class PortScanner:
    def __init__(self, ip: str, start_port: int, end_port: int, protocol: str = 'tcp', timeout: float = 1.0) -> None:
        self.ip = ip
        self.start_port = start_port
        self.end_port = end_port
        self.protocol = protocol
        self.timeout = timeout

    def get_service_name(self, port: int) -> str:
        """Return the service name for the given port."""
        return service_names.get(port, "Unknown Service")

    def scan_port(self, port: int) -> None:
        """Scan a single port."""
        try:
            if self.protocol == 'tcp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.ip, port))
                if result == 0:
                    service = self.get_service_name(port)
                    with print_lock:
                        print(f"Port {port} (TCP) is open - {service}")
            elif self.protocol == 'udp':
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(self.timeout)
                sock.sendto(b'', (self.ip, port))  # Send a blank packet
                try:
                    sock.recvfrom(1024)  # Wait for a response
                    service = self.get_service_name(port)
                    with print_lock:
                        print(f"Port {port} (UDP) is open - {service}")
                except socket.timeout:
                    pass
            sock.close()
        except Exception as e:
            with print_lock:
                print(f"Error scanning port {port}: {e}")

    def start_scan(self) -> None:
        """Scan a range of ports on the given IP address."""
        threads = []
        for port in range(self.start_port, self.end_port + 1):
            thread = Thread(target=self.scan_port, args=(port,))
            thread.start()
            threads.append(thread)

            # Optional: Rate limiting
            time.sleep(0.01)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

class PortScannerCLI:
    @staticmethod
    def _get_version() -> str:
        """Get the installed package version or return the hardcoded version."""
        try:
            return version('pyscan-tool') 
        except PackageNotFoundError:
            return __version__

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="Port Scanner Tool")
        self.configure_arguments()

    def configure_arguments(self) -> None:
        """Set up command line arguments."""
        self.parser.add_argument('-ip', '--ip-address', help="IP address to scan")
        self.parser.add_argument('-r', '--range', help="Port range to scan (e.g., 80-443)")
        self.parser.add_argument('-p', '--protocol', choices=['tcp', 'udp'], default='tcp', help="Protocol to use (default: tcp)")
        self.parser.add_argument('-t', '--timeout', type=float, default=1.0, help="Timeout in seconds (default: 1.0)")
        self.parser.add_argument('-v', '--version', action='version', version=self._get_version(), help="Show program's version number and exit")

    def get_arguments(self) -> argparse.Namespace:
        """Parse and return command line arguments."""
        return self.parser.parse_args()

    def prompt_for_missing_arguments(self, args: argparse.Namespace) -> tuple[str, int, int, str, float]:
        """Prompt the user for missing arguments with default values."""
        if not args.ip_address:
            # Provide default value 'localhost' if user presses Enter
            args.ip_address = input("Enter the IP address to scan : ") or "localhost"

        if not args.range:
            # Provide default value '80-443' if user presses Enter
            args.range = input("Enter the port range (e.g 80-443) : ") or "80-443"

        start_port, end_port = map(int, args.range.split('-'))
        return args.ip_address, start_port, end_port, args.protocol, args.timeout


    def run(self) -> None:
        """Run the port scanner based on command line inputs."""
        args = self.get_arguments()
        ip, start_port, end_port, protocol, timeout = self.prompt_for_missing_arguments(args)

        print(f"Scanning {ip} for {protocol.upper()} ports from {start_port} to {end_port}...")
        scanner = PortScanner(ip, start_port, end_port, protocol, timeout)
        scanner.start_scan()

def main() -> None:
    cli = PortScannerCLI()
    cli.run()

if __name__ == "__main__":
    main()
