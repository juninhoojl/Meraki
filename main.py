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



## RASCUNHO
def teste(chave, organizacao):

    url = "https://api.meraki.com/api/v1/organizations/{}/policyObjects".format(organizacao)
    
    payload = {"name":"Test Object","category":"network", "type": "cidr", "cidr":"10.0.0.0/24","groupIds":[]}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": chave
    }

    oganizations = requests.request('POST', url, headers=headers, data=json.dumps(payload))
    oganizations_parsed = json.loads(oganizations.text)
    print(oganizations_parsed)

