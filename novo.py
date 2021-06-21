from logging import setLoggerClass
import os
from dotenv import load_dotenv
import requests
from requests import Session
import json

class NoRebuildAuthSession(Session):
    def rebuild_auth(self, prepared_request, response):
        pass

class MerakiAPI:
    def __init__(self, chave):
        self.__sessao = NoRebuildAuthSession()
        self.__baseURL = 'https://api.meraki.com/api/v1'
        self.__payload = None
        self.__headers = {'Authorization': f'Bearer {chave}'}

    def requesicao(self, url): # Adicionar o exception
        try:
            return self.__sessao.get(self.__baseURL+url, headers=self.__headers, data=self.__payload, timeout=5).json()
        except:
            return 'Erro'

    def putrequest(self, url, payload): # Adicionar o exception
        return self.__sessao.put(self.__baseURL+url, headers=self.__headers, data=payload, timeout=5)

    def getOrganizacoes(self):
        return self.requesicao("/organizations/")

    def getOrganizacao(self, id_organizacao):
        return self.requesicao("/organizations/{}/".format(id_organizacao))

    def getRedes(self, id_organizacao):
        return self.requesicao("/organizations/{}/networks".format(id_organizacao))

    def getRede(self, id_rede):
        return self.requesicao("/networks/{}/".format(id_rede))

    def getDevices(self, id_rede):
        return self.requesicao("/networks/{}/devices".format(id_rede))

    def getDevice(self, serial_device):
        return self.requesicao("/devices/{}/".format(serial_device))

    def getClientes(self, serial_device):
        return self.requesicao("/devices/{}/clients/".format(serial_device))
    
    def getClientesRede(self, id_rede):
        return self.requesicao("/networks/{}/clients".format(id_rede))

    def getClientPolicy(self, id_rede, id_cliente):
        return self.requesicao("/networks/{}/clients/{}/policy".format(id_rede,id_cliente))
        

    def getInterfaces(self, serial_device):
        return self.requesicao("/devices/{}/managementInterface".format(serial_device))

    # def updateNetwork(self, id_rede, payload):
    #     return self.putrequest("/networks/{}/".format(id_rede), payload)

    # def getPolicyObjects(self, id_organizacao):
    #     return self.requesicao("/organizations/{}/policyObjects/".format(id_organizacao))

    # def getGroupPolicies(self, id_rede):
    #     return self.requesicao("/networks/{}/groupPolicies/".format(id_rede))

    # def createObject(self, id_organizacao, payload):
    #     return self.putrequest("/organizations/{}/policyObjects".format(id_organizacao), payload)

def printa(jsonDado):
    print(json.dumps(jsonDado, indent=4, sort_keys=True))

def teste(chave, organizacao):

    url = "https://api.meraki.com/api/v1/organizations/{}/policyObjects".format(organizacao)
    payload = {"name":"Test Object","category":"network", "type": "cidr", "cidr":"10.0.0.0/24","groupIds":[]}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": chave
    }

    oganizations = requests.request('PUT', url, headers=headers, data = payload)
    oganizations_parsed = json.loads(oganizations.text)
    print(oganizations_parsed)

def teste_acha_grupo(chave, meraki):

    listaRedes = []
    for org in meraki.getOrganizacoes():
     # So vai pode ter group policy redes que tem tipo de produto appliance e/ou wireless
        for x in meraki.getRedes(org['id']):
            try:
                if 'appliance' in x['productTypes'] or 'wireless' in x['productTypes']:
                    if len(meraki.getGroupPolicies(x['id'])) > 0:
                        listaRedes.append[x['id']]
                        break
            except:
                pass

        if len(listaRedes) > 0:
            break
    print(listaRedes)

if __name__ == '__main__':
    load_dotenv()
    meraki = MerakiAPI(os.environ.get("APIKEY"))
    #print(meraki.getOrganizacoes())
    #print(json.dumps(meraki.getRedes(681155), indent=4, sort_keys=True))
    

    #print(json.dumps(meraki.getRede('L_566327653141843049'), indent=4, sort_keys=True))
    #print(json.dumps(meraki.getDevices('L_566327653141843049'), indent=4, sort_keys=True))
    #print(json.dumps(meraki.getDevice('Q2SW-SWQ2-HZ9L'), indent=4, sort_keys=True))
    #print(json.dumps(meraki.getInterfaces('Q2SW-SWQ2-HZ9L'), indent=4, sort_keys=True))
    #print(json.dumps(meraki.getClientes('Q2SW-SWQ2-HZ9L'), indent=4, sort_keys=True))

    #payloadObject = {"name":"Test Object","category":"network", "type": "cidr", "cidr":"10.0.0.0/24","groupIds":[]}
    #retorno = meraki.createObject(681155, payloadObject)

    #objetos = meraki.getPolicyObjects(575334852396583244)
    #print(retorno)
    #print(json.dumps(meraki.getGroupPolicies('N_566327653141899127'), indent=4, sort_keys=True))


    # teste_acha_grupo(os.environ.get("APIKEY"), meraki)
   
    #print(json.dumps(meraki.getClientes('Q2SW-SWQ2-HZ9L'), indent=4, sort_keys=True))

    printa(meraki.getRedes(681155))
    for rede in meraki.getRedes(681155):
        print('--'*20)
        print('Rede: ', rede['id'])
        print('--'*20)
        printa(meraki.getClientesRede(rede['id']))
    #printa(meraki.getClientPolicy('N_566327653141899127','k5a5804'))

    