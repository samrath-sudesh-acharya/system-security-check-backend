import os
import hashlib
from virustotal_python import Virustotal
from pymongo import MongoClient

# Function to calculate the file's SHA256 hash
def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

# Function to scan a file with VirusTotal
def scan_file(file_path):

    # Set your VirusTotal API key
    API_KEY = 'b09a615cf8e528e3567a39cee1ab054da16b1778af0ef190fa52adf85740240d'

    # Create a Virustotal object
    vt = Virustotal(API_KEY)

    # Calculate the file's SHA256 hash
    file_hash = calculate_sha256(file_path)
    # Check if the file has already been scanned
    try:
        response = vt.request(f"files/{file_hash}")
        print(f"\n\nFILE:{file_path}\n\n")
        if response.data:  # Check if response.data is a non-empty list
            print(response.data)

            connection_string = "mongodb+srv://demo:samrath@cluster0.o0foj0z.mongodb.net/?retryWrites=true&w=majority"
            database_name = "scan_folder"
            collection_name = "sus_folder"

            client = MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)
            db = client[database_name]
            collection = db[collection_name]

            # Insert the rules dictionary
            collection.insert_one(response.data)
    except:
        pass

