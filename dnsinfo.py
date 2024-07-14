import socket
import dns.resolver
import requests
import argparse

def get_ip_address(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def get_dns_records(domain):
    records = {}
    record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SRV']
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [str(record) for record in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            records[record_type] = []
    return records

def get_server_details(domain):
    try:
        response = requests.get(f'http://{domain}', timeout=5)
        return response.headers.get('Server', 'N/A')
    except requests.RequestException:
        return 'N/A'

def enumerate_subdomains(domain):
    subdomains = []
    common_subdomains = ['www', 'mail', 'ftp', 'blog', 'api', 'test']
    for sub in common_subdomains:
        subdomain = f"{sub}.{domain}"
        if get_ip_address(subdomain):
            subdomains.append(subdomain)
    return subdomains

def gather_domain_info(domain):
    def green(text):
        return f"\033[92m{text}\033[0m"

    def bold(text):
        return f"\033[1m{text}\033[0m"
    
    print(green(f"\n● Gathering information for domain: {bold(domain)}"))
    
    ip_address = get_ip_address(domain)
    print(green(f"● IP Address: ") + f"{ip_address if ip_address else 'Not found'}")
    
    dns_records = get_dns_records(domain)
    print(green("● DNS Records:"))
    for record_type, records in dns_records.items():
        print(f"  {bold(record_type)}: {', '.join(records) if records else 'None'}")
    
    server_details = get_server_details(domain)
    print(green(f"● Server Details: ") + f"{server_details}")
    
    subdomains = enumerate_subdomains(domain)
    print(green("● Subdomains:"))
    print(", ".join(subdomains) if subdomains else "None found")

def main():
    parser = argparse.ArgumentParser(description='Gather DNS information for a domain')
    parser.add_argument('domain', help='The domain to gather information for')
    args = parser.parse_args()
    gather_domain_info(args.domain)

if __name__ == "__main__":
    main()
