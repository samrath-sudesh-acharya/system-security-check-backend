import subprocess
import re
import json

def get_arp_table():
    arp_result = subprocess.check_output("arp -a").decode()
    arp_entries = arp_result.splitlines()

    arp_table = []
    columns = ["Internet Address", "Physical Address", "Type"]
    pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)\s+([a-fA-F0-9-]+)\s+(\w+)")

    for entry in arp_entries[1:]:
        match = re.match(pattern, entry)
        if match:
            arp_entry = dict(zip(columns, match.groups()))
            arp_table.append(arp_entry)

    return arp_table

# Call the get_arp_table function to obtain the ARP table data
arp_table = get_arp_table()

# Convert the ARP table to JSON format
arp_json = json.dumps(arp_table, indent=4)
print(arp_json)
