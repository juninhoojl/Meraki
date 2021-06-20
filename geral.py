import os
from dotenv import load_dotenv
import requests
import json


# Organizations consist of Networks, which then contain Devices.
# Tendo em mente isso vou listar todas as organizacoes e detalhes
# escolher uma organizacao arbitrariamente e usar o id dela para listar as redes dela

# Carrega variaveis de ambiente
load_dotenv() 

# Request organziations details

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

#print(json.dumps(networks_parsed[0], indent=4, sort_keys=True))

# agora tendo a rede vou listar os dispositivos dela
id_rede = networks_parsed[0]['id']


url3 = baseUrl+"/networks/{}/devices".format(id_rede)

devices = requests.request('GET', url3, headers=headers, data=payload)
devices_parsed = json.loads(devices.text)

# Aqui tenho o primeiro dispositivo da primeira rede da primeira organizacao encontrada
#print(json.dumps(devices_parsed[0], indent=4, sort_keys=True))

# Agora tendo informacoes gerais sobre esse dipositivo podemos ver outras infomacoes
# Como as informacoes sobre as interfaces
# Use the serial from the /networks/:networkId/devices response as the :
# serial in the following request to determine whether it has been assigned a dynamic or static IP address.

device_serial = devices_parsed[0]['serial']

url4 = baseUrl+"/devices/{}/managementInterface".format(device_serial)

interfaceInfo = requests.request('GET', url4, headers=headers, data=payload)
interfaceInfo_parsed = json.loads(interfaceInfo.text)

print(json.dumps(interfaceInfo_parsed, indent=4, sort_keys=True))


