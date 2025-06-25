import sys
import pyfiglet
from termcolor import colored
from colorama import init
import requests
import threading
init()

ascii_banner = pyfiglet.figlet_format("Subdomain\nEnumeration Tool")
colored_banner = colored(ascii_banner, color="red")
print(colored_banner)
if len(sys.argv) != 2:
    print(colored("[!] Usage: python3 subdomain_enumeration_tool.py <domain>", color="yellow"))
    sys.exit(1)
domain = sys.argv[1]
try:
    with open('subdomains.txt') as file:
        subdomains = file.read().splitlines()
except FileNotFoundError:
    print(colored("[!] Error: 'subdomains.txt' file not found.", color="red"))
    sys.exit(1)

discovered_subdomains = []
lock = threading.Lock()

def check_subdomain(subdomain):
    url = f"http://{subdomain}.{domain}"
    try:
        requests.get(url, timeout=5)
    except requests.ConnectionError:
        pass
    else:
        print(colored(f"[+] Discovered subdomain: {url}", color="green"))
        with lock:
            discovered_subdomains.append(url)

threads = []

for subdomain in subdomains:
    thread = threading.Thread(target=check_subdomain, args=(subdomain,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
with open("discovered_subdomains.txt", 'w') as f:
    for subdomain in discovered_subdomains:
        f.write(subdomain + "\n")

print(colored("\n[✓] Enumeration complete. Results saved in 'discovered_subdomains.txt'", color="cyan"))
