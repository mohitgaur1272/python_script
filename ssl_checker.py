import socket
import ssl
import sys

def check_ssl(subdomain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((subdomain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=subdomain) as ssock:
                return f"SSL certificate is valid for {subdomain}"
    except ssl.CertificateError as e:
        return f"SSL certificate is not valid for {subdomain}: {e}"
    except ssl.SSLError as e:
        return f"No SSL certificate found for {subdomain}: {e}"
    except Exception as e:
        return f"An error occurred while checking SSL for {subdomain}: {e}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py domains.txt")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            subdomains = f.readlines()
            subdomains = [subdomain.strip().replace("https://", "").replace("http://", "") for subdomain in subdomains]
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        sys.exit(1)

    for subdomain in subdomains:
        result = check_ssl(subdomain)
        print(result)

if __name__ == "__main__":
    main()

