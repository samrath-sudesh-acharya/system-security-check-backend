from port_scanner import scan_port, get_ip_address
from scan import scan_windows_filesystem
from firewall import save_rules_to_json, save_rules_to_mongodb
from mitm import detect_mitm_attack
from password import execute_program
import concurrent.futures
from IPy import IP
import socket
import json

def start():
    # Get the target IP address
    target = get_ip_address()

    try:
        ip = IP(target)
    except ValueError:
        ip = socket.gethostbyname(target)

    start_port, end_port = 1, 1000

    print(f"Scanning ports for IP: {ip}")

    # Create a ThreadPoolExecutor with the desired number of threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create a list to store the futures for each task
        futures = []

        # Run port scanning using parallelism
        port_range = range(start_port, end_port + 1)
        for port in port_range:
            futures.append(executor.submit(scan_port, str(ip), port))

        print("Port scanning in progress...")

        # Run virus scanning using parallelism
        futures.append(executor.submit(scan_windows_filesystem))
        print("Virus scanning in progress...")

        # Run firewall rule saving using parallelism
        rules = executor.submit(save_rules_to_json)
        futures.append(executor.submit(save_rules_to_mongodb, json.dumps(rules.result())))
        print("Firewall rule saving in progress...")

        # Run MITM attack detection using parallelism
        futures.append(executor.submit(detect_mitm_attack))
        print("MITM attack detection in progress...")
        
        futures.append(executor.submit(execute_program))

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            # Retrieve the result of each future to ensure exceptions are raised
            _ = future.result()

    print("All tasks completed.")

# Start the scanning and detection processes
start()
