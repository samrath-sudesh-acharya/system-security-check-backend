import subprocess
import json
from pymongo import MongoClient


def save_rules_to_mongodb(rules_json):

    connection_string = "mongodb+srv://demo:samrath@cluster0.o0foj0z.mongodb.net/?retryWrites=true&w=majority"
    database_name = "secruity_check"
    collection_name = "firewall_rule"

    # Convert JSON document to dictionary
    rules_dict = json.loads(rules_json)

    # Connect to MongoDB Atlas
    client = MongoClient(connection_string,tls=True,
                             tlsAllowInvalidCertificates=True)
    db = client[database_name]
    collection = db[collection_name]
    
    # Insert the rules dictionary
    collection.insert_many(rules_dict)



def save_rules_to_json():
    """ Save firewall rules to a JSON file """
    output = subprocess.check_output(
        "netsh advfirewall firewall show rule name=all",
        shell=True,
        stderr=subprocess.DEVNULL
    ).decode()

    # Process the output to extract rule information
    rule_lines = [line.strip() for line in output.splitlines() if line.strip()]
    rules = []
    current_rule = {}
    for line in rule_lines:
        if line.startswith("Rule Name:"):
            if current_rule:
                rules.append(current_rule)
            current_rule = {"Rule Name": line.split(":")[1].strip()}
        elif ":" in line:
            key, value = [item.strip() for item in line.split(":", 1)]
            if key != "----------------------------------------------------------------------":
                current_rule[key] = value

    # Add the last rule to the list
    if current_rule:
        rules.append(current_rule)

    return rules


    

