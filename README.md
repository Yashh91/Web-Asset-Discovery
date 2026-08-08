#  Web Asset Discovery Tool

A Python tool for discovering subdomains, IP addresses, and basic web information from a domain.

##  Features

* Subdomain enumeration using a custom wordlist
* DNS resolution
* IP address discovery
* HTTP/HTTPS detection
* HTTP status-code detection
* Page-title extraction
* Multithreaded scanning
* Custom wordlist support
* Configurable thread count
* Save results to a file
* Simple command-line interface

##  Installation

Clone the repository:

```bash
git clone https://github.com/Yashh91/Web-Asset-Discovery.git
```

Open the project folder:

```bash
cd Web-Asset-Discovery
```

Install the required dependency:

```bash
pip install -r requirements.txt
```

##  Usage

### Basic Scan

```bash
python web_asset_discovery.py -d example.com
```

### Custom Wordlist

```bash
python web_asset_discovery.py -d example.com -w wordlist.txt
```

### Custom Threads

```bash
python web_asset_discovery.py -d example.com -t 30
```

### Save Results

```bash
python web_asset_discovery.py -d example.com -o results.txt
```

### Use All Options

```bash
python web_asset_discovery.py -d example.com -w wordlist.txt -t 30 -o results.txt
```

##  Command-Line Options

| Option             | Description            |
| ------------------ | ---------------------- |
| `-d`, `--domain`   | Target domain          |
| `-w`, `--wordlist` | Subdomain wordlist     |
| `-t`, `--threads`  | Number of threads      |
| `-o`, `--output`   | Save results to a file |
| `-h`, `--help`     | Show help information  |

##  Screenshots

### Tool Banner

<img width="1207" height="302" alt="image" src="https://github.com/user-attachments/assets/47a0abba-c05e-4311-b8fc-13b77288437b" />

### Asset Discovery

<img width="1280" height="625" alt="image" src="https://github.com/user-attachments/assets/ef3de7c5-a6e5-462e-abd3-244081e15e63" />

### Saved Results

<img width="1087" height="295" alt="image" src="https://github.com/user-attachments/assets/5982b009-1033-496a-9efd-622b8f3324ab" />

##  License

This project is licensed under the MIT License.
