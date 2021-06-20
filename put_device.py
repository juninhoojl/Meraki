import os
from dotenv import load_dotenv
import requests
import json

load_dotenv() 

baseUrl = 'https://api.meraki.com/api/v1'
url = baseUrl+'/organizations'
payload = None

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": os.environ.get("APIKEY")
}

oganizations = requests.request('GET', url, headers=headers, data = payload)
oganizations_parsed = json.loads(oganizations.text)

# for i in parsed:
#     print(i['id'])

id_organizacao = oganizations_parsed[0]['id']
#print(id_organizacao)

# Listando as redes de uma organizacao

url2 = baseUrl+"/organizations/{}/networks".format(id_organizacao)

networks = requests.request('GET', url2, headers=headers, data = payload)
networks_parsed = json.loads(networks.text)

id_rede = networks_parsed[0]['id']

url3 = baseUrl+"/networks/{}/devices".format(id_rede)

devices = requests.request('GET', url3, headers=headers, data=payload)
devices_parsed = json.loads(devices.text)


device_serial = devices_parsed[0]['serial']

# Mostra informacao device
print(json.dumps(devices_parsed[0], indent=4, sort_keys=True))

# Aqui vou alterar o nome dele
informacao_geral = devices_parsed[0]
print(informacao_geral['name'])

urlPut = baseUrl+"/devices/{}".format(device_serial)

novosDados = {
    "name": "Novo Nome",
    "lat": 37.4180951010362,
    "lng": -122.098531723022,
    "serial": informacao_geral['serial'],
    "mac": informacao_geral['mac'],
    "tags": informacao_geral['tags']
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": os.environ.get("APIKEY")
}

response = requests.request('PUT', urlPut, headers=headers, data = json.dumps(novosDados))

print(response.status_code)



