import re
import json
import subprocess

# data = """
# Interface: 192.168.72.169 --- 0x7
#   Internet Address      Physical Address      Type
#   192.168.72.234        2a-38-3c-75-1f-3c     dynamic
#   192.168.72.255        ff-ff-ff-ff-ff-ff     static
#   224.0.0.22            01-00-5e-00-00-16     static
#   239.255.255.250       01-00-5e-7f-ff-fa     static
#   255.255.255.255       ff-ff-ff-ff-ff-ff     static
# """

arp_result = subprocess.check_output("arp -a").decode()

lines = arp_result.strip().split('\n')
headers = re.split(r'\s{2,}', lines[1].strip())
result = []

for line in lines[2:]:
    values = re.split(r'\s{2,}', line.strip())
    entry = dict(zip(headers, values))
    result.append(entry)

json_output = json.dumps(result, indent=2)
print(json_output)
