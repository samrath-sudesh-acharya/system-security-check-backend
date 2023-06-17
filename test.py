
import pymongo 

uri = "mongodb+srv://demo:samrath@cluster0.o0foj0z.mongodb.net/?retryWrites=true&w=majority"

# Create the MongoClient with SSL options
client = pymongo.MongoClient(uri,tls=True,
                             tlsAllowInvalidCertificates=True)

mydb = client['open_ports']
# print(mydb['storez'])

# mydb['storez'].insert_one({
#         "Rule Name": "Microsoft Edge (mDNS-In)",
#         "Enabled": "Yes",
#         "Direction": "In",
#         "Profiles": "Domain,Private,Public",
#         "Grouping": "Microsoft Edge WebView2 Runtime",
#         "LocalIP": "Any",
#         "RemoteIP": "Any",
#         "Protocol": "UDP",
#         "LocalPort": "5353",
#         "RemotePort": "Any",
#         "Edge traversal": "No",
#         "Action": "Allow"
#     })

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)