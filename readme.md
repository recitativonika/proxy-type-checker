# Proxy type checker

## Description
This Python script checks the validity of proxies by attempting to connect and determines whether each proxy is a Datacenter or Residential proxy. 

## Features
- **Check Proxy active or not and auto save to datacenter.txt or residental.txt depending the proxy type**

## Prerequisites
- [Python](https://www.python.org) (Version 3.6 or higher)

## Installation

1. Clone the repository to your local machine:
   ```bash
	git clone https://github.com/recitativonika/proxy-type-checker.git
   ```
2. Navigate to the project directory:
	```bash
	cd proxy-type-checker
	```
3. Install the necessary dependencies:
	```bash
	pip install -r requirements.txt
	```

## Usage

1. Put your proxy list in `proxy.txt` before running the script. example below:
	```
	ip:port
	username:password@ip:port
	http://ip:port
	http://username:password@ip:port
	socks5://ip:port
	socks5://username:password@ip:port
	```

2. Run the script:
	```bash
	python main.py
	```
3. The script will check if proxy is valid/active or not and save the proxy list in `residental.txt` or `datacenter.txt` depend of the proxy type.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Note
This script only for testing purpose.