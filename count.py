import re
import warnings

def count_requests_for_domains(log_file, domain_file):
    request_counts = {}
    with open(log_file, 'r') as file:
        with open(domain_file, 'r') as domain_file:
            domains = [line.strip() for line in domain_file]

            for line in file:
                for domain in domains:
                    if re.search(domain, line):
                        request_counts[domain] = request_counts.get(domain, 0) + 1
    return request_counts

if __name__ == "__main__":
    log_file = "access.log"  # Path to your Apache access log file
    domain_file = "domains.txt"  # Path to the file containing the list of domains

    # Suppress warnings
    warnings.filterwarnings("ignore")

    request_counts = count_requests_for_domains(log_file, domain_file)
    for domain, count in request_counts.items():
        print(f"Request count for {domain} in {log_file}: {count}")
