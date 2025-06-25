import sys
import pyfiglet
from termcolor import colored
from colorama import init
import dns.resolver
init()
ascii_banner = pyfiglet.figlet_format("DNS Enumeration Tool")
colored_banner = colored(ascii_banner, color="yellow")
print(colored_banner)
if len(sys.argv) != 2:
    print(colored("[!] Usage: python3 dns_enum.py <domain>", color="red"))
    sys.exit(1)

target_domain = sys.argv[1]

records_type = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'SOA']

resolver = dns.resolver.Resolver()

for record_type in records_type:
    try:
        answer = resolver.resolve(target_domain, record_type)
    except dns.resolver.NoAnswer:
        print(colored(f"[-] No {record_type} record found for {target_domain}", color="blue"))
        continue
    except dns.resolver.NXDOMAIN:
        print(colored(f"[!] Domain {target_domain} does not exist!", color="red"))
        break
    except dns.exception.Timeout:
        print(colored(f"[!] Timeout while querying {record_type} record for {target_domain}", color="red"))
        continue
    except dns.resolver.NoNameservers:
        print(colored(f"[!] No nameservers available for {target_domain}", color="magenta"))
        break
    except Exception as e:
        print(colored(f"[!] Unexpected error for {record_type} record: {str(e)}", color="red"))
        continue

    print(colored(f"\n{record_type} records for {target_domain}:", color="green"))
    for data in answer:
        print(f"  {data}")
