import os
from dotenv import load_dotenv
import requests
import json

# Carrega variaveis de ambiente
load_dotenv() 

serial = 'Q2QN-9J8L-SLPD'
url = "https://api.meraki.com/api/v1/devices/{}".format(serial)

payload = None

# Chave vinda do .env
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": os.environ.get("APIKEY")
}

# Ja recebe em utf8
response = requests.request('GET', url, headers=headers, data = payload)
print('- ' * 30)
parsed = json.loads(response.text)
print(json.dumps(parsed, indent=4, sort_keys=True))
