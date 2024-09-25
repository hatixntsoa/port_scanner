# PyScan Tool

<p align="center">
 <img height="150" src="https://raw.githubusercontent.com/h471x/port_scanner/master/imgs/pyscan.png"/>
</p>

<div align="center">

<p>

``pyscan-tool`` is a Python-based port scanning utility that allows users to scan for open ports on a specified IP address. It provides options for scanning TCP and UDP ports, identifying services associated with each open port, and offering a command-line interface for ease of use.

</p>

### Contents

[Features](#features) |
[Installation](#installation) |
[Build from scratch](#option-2-build-from-source) |
[Usage](#usage) |
[Development](#development) |
[Contributing](#contributing)

</div>

## Features

- **Command-Line Interface (CLI)**: The default interface for scanning ports directly from the terminal.
- **Service Name Identification**: Automatically identifies and displays the service associated with each open port.
- **TCP and UDP Scanning**: Options to scan for both TCP and UDP ports.
- **Configurable Timeout**: Users can specify the timeout duration for connection attempts.

## Installation

### Option 1: Install from PyPI

To install `pyscan-tool` directly from PyPI:

```bash
pip install pyscan-tool
```

### Option 2: Build from Source

For those who prefer to build it themselves:

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/h471x/port_scanner.git
   cd port_scanner
   ```

2. Build the package:

   ```bash
   python setup.py sdist bdist_wheel
   ```

3. Install the package:

   ```bash
   pip install dist/*.whl
   ```

## Usage

Once the package is installed, you can use the `pyscan` command from the terminal. The script accepts the following command-line arguments:

- **IP Address**:
  - `-ip` or `--ip-address`: Specify the IP address to scan.
  
- **Port Range**:
  - `-r` or `--range`: Specify the port range to scan (e.g., `80-443`).

- **Protocol**:
  - `-p` or `--protocol`: Specify the protocol to use (`tcp` or `udp`). Default is `tcp`.

- **Timeout**:
  - `-t` or `--timeout`: Specify the timeout duration in seconds. Default is `1.0`.

### Example Usage

1. **Basic Scan**:
   ```bash
   pyscan -ip <ip_address> -r 80-443
   ```

2. **Specify Protocol and Timeout**:
   ```bash
   pyscan -ip <ip_address> -r 1-100 -p udp -t 2
   ```

3. **Help Option**:
   For help with command-line options, use:
   ```bash
   pyscan -h
   ```

## Development

To modify or extend the functionality, ensure you have the required dependencies installed. You can add new features to the CLI as needed.

## Contributing

Feel free to fork this repository, open issues, or submit pull requests with improvements or bug fixes. Your contributions help make the `PyScan Tool` better!