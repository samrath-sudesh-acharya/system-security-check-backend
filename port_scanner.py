import socket
from pymongo import MongoClient

#Fetch the system's IP address
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# Function to scan open ports and detect services
def scan_port(ip, port):
    conn = MongoClient("mongodb+srv://demo:samrath@cluster0.o0foj0z.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
    db = conn["open_ports"]
    collection = db["storez"]
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set a timeout value for the connection attempt
        sock.settimeout(0.5)

        # Attempt to connect to the target IP address and port
        result = sock.connect_ex((ip, port))

        if result == 0:
            # Attempt to receive banner information from the service
            banner = sock.recv(1024).decode().strip()
            print(f'Service running on port {port}: {banner}')
            info = {"Port": port, "Banner": banner}
            collection.insert_one(info)

        sock.close()
    #If we don't find a banner for a open port we print the port number
    except Exception as e:
         info_1={"Port":port}
         collection.insert_one(info_1)


