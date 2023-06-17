from pymongo import MongoClient

# Connect to MongoDB Atlas
db = MongoClient("mongodb+srv://demo:samrath@cluster0.o0foj0z.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)


# Delete data from collections
db["Victim"]["users"].delete_many({})
db["mitm"]["arp_table"].delete_many({})
db["mitm"]["attack_details"].delete_many({})
db["open_ports"]["storez"].delete_many({})
db["scan_folder"]["sus_folder"].delete_many({})
db["secruity_check"]["firewall_rule"].delete_many({})

# Optional: Drop collections (if needed)
# db["users"].drop()
# db["arp_table"].drop()
# db["attack_details"].drop()
# db["strez"].drop()
# db["sus_folder"].drop()
# db["firewall_rule"].drop()

print("Data deleted successfully.")
