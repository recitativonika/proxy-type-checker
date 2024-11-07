import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
import yaml
import sys
import signal

# Initialize colorama
init(autoreset=True)

def signal_handler(sig, frame):
    print("\nExiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config.get('limit_workers', 100)

def check_proxy(proxy):
    proxy_dict = {
        "http": proxy,
        "https": proxy,
    }
    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxy_dict, timeout=10)
        if response.status_code != 200:
            return proxy, "Failed to connect"

        ip_info = response.json()
        origin_ip = ip_info.get("origin", "Unknown")

        if origin_ip == proxy.split(':')[0]:
            return proxy, "Datacenter"
        else:
            return proxy, "Residential"
    except requests.exceptions.ProxyError:
        return proxy, "Failed to connect"
    except requests.exceptions.Timeout:
        return proxy, "Timeout"
    except ValueError:
        return proxy, "Invalid response"
    except Exception as e:
        print(f"{Fore.RED}Error checking proxy {proxy}: {e}{Style.RESET_ALL}")
        return proxy, "Unknown"

def save_to_file(proxy, proxy_type):
    if proxy_type not in ["Datacenter", "Residential"]:
        return
    
    filename = "datacenter.txt" if proxy_type == "Datacenter" else "residential.txt"
    
    try:
        with open(filename, "r") as file:
            existing_proxies = file.read().splitlines()
    except FileNotFoundError:
        existing_proxies = []

    if proxy not in existing_proxies:
        with open(filename, "a") as file:
            file.write(f"{proxy}\n")

def main():
    proxy_file = "proxy.txt"
    with open(proxy_file, "r") as file:
        proxies = [proxy.strip() for proxy in file.readlines()]

    # Load max_workers from config.yaml
    max_workers = load_config()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        
        for future in as_completed(future_to_proxy):
            proxy, proxy_type = future.result()
            
            if proxy_type == "Datacenter":
                type_color = Fore.YELLOW
                proxy_color = Fore.YELLOW
            elif proxy_type == "Residential":
                type_color = Fore.GREEN
                proxy_color = Fore.GREEN
            elif proxy_type == "Failed to connect":
                type_color = Fore.RED
                proxy_color = Fore.RED
            else:
                type_color = Fore.WHITE
                proxy_color = Fore.WHITE
            
            if proxy_type == "Unknown":
                proxy_color = Fore.RED
                type_color = Fore.RED
            
            print(f"Proxy: {proxy_color}{proxy}{Style.RESET_ALL}, Type: {type_color}{proxy_type}{Style.RESET_ALL}")
            save_to_file(proxy, proxy_type)

if __name__ == "__main__":
    main()
