import subprocess
import socket
import re
from pymongo import MongoClient

def get_arp_table_2():
    arp_result = subprocess.check_output("arp -a").decode()

    lines = arp_result.strip().split('\n')
    headers = re.split(r'\s{2,}', lines[1].strip())
    result = []

    for line in lines[2:]:
        values = re.split(r'\s{2,}', line.strip())
        entry = dict(zip(headers, values))
        result.append(entry)
    return result

def get_arp_table():
    arp_result = subprocess.check_output("arp -a").decode()
    arp_entries = arp_result.splitlines()

    arp_table = []
    columns = ["Internet Address", "Physical Address", "Type"]
    pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)\s+([a-fA-F0-9-]+)\s+(\w+)")

    for entry in arp_entries[1:]:
        match = re.match(pattern, entry)
        print(entry)
        if match:
            arp_entry = dict(zip(columns, match.groups()))
            arp_table.append(arp_entry)
    
    if (arp_table == []):
        arp_table = get_arp_table_2()

    return arp_table

def detect_mitm_attack():
    # Connect to MongoDB Atlas
    conn = MongoClient("mongodb+srv://demo:samrath@cluster0.o0foj0z.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
    db = conn["mitm"]
    collection1 = db["arp_table"]
    collection2 = db["attack_details"]
    arp_table = get_arp_table()

    internal_ip_addresses = set()
    attack_details = []

    for entry in arp_table:
        ip_address = entry["ip_address"]
        mac_address = entry["mac_address"]

        if ip_address.startswith("192.168."):  # Consider only internal IP addresses
            if ip_address in internal_ip_addresses:
                # Found two internal IP addresses with the same MAC address
                attack_details.append({
                    "ip_address": ip_address,
                    "mac_address": mac_address,
                    "mitm_attack": True
                })
            else:
                internal_ip_addresses.add(ip_address)

    # Store ARP table in MongoDB
    collection1.insert_many(arp_table)

    # Store attack details in MongoDB
    collection2.insert_many(attack_details)
