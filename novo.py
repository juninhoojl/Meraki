import os
from dotenv import load_dotenv
import requests
from requests import Session
import json

# Rescrevendo o rebuild ocm pass para autenticar so quando for instaciado
class NoRebuildAuthSession(Session):

    #Lembrar para usar ele se quiser super.rebuild_auth(self, prepared_request, response):
    def rebuild_auth(self, prepared_request, response):
        pass

    # RASCUNHOOOO
    def reauth(self, prepared_request, response):
        super.rebuild_auth(self, prepared_request, response)

class MerakiAPI:
    def __init__(self, chave):
        self.__sessao = NoRebuildAuthSession()
        self.__baseURL = 'https://api.meraki.com/api/v1'
        self.__payload = None
        self.__headers = {'Authorization': f'Bearer {chave}', "Content-Type": "application/json", "Accept": "application/json"}

    def requesicao(self, url):
        try:
            return self.__sessao.get(self.__baseURL+url, headers=self.__headers, data=self.__payload, timeout=5).json()
        except:
            return 'Erro'

    def postrequest(self, url, payload):
        try:
            return self.__sessao.post(self.__baseURL+url, headers=self.__headers, data=json.dumps(payload), timeout=5).json()
        except:
            return 'Erro'

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

    def getPoliticasRede(self, id_rede):
        return self.requesicao("/networks/{}/groupPolicies".format(id_rede))

    def getInterfaces(self, serial_device):
        return self.requesicao("/devices/{}/managementInterface".format(serial_device))

    def updateNetwork(self, id_rede, payload):
        return self.putrequest("/networks/{}/".format(id_rede), payload)

    def getPolicyObjects(self, id_organizacao):
        return self.requesicao("/organizations/{}/policyObjects/".format(id_organizacao))

    def getGroupPolicies(self, id_rede):
        return self.requesicao("/networks/{}/groupPolicies/".format(id_rede))

    def createObject(self, id_organizacao, payload):
        return self.postrequest("/organizations/{}/policyObjects".format(id_organizacao), payload)

    # Lista grupos de objetos existentes
    def getPolicyObjGroup(self, id_organizacao):
        return self.requesicao("/organizations/{}/policyObjects/groups".format(id_organizacao))

    # Cria novo grupo
    def postPolicyObjGroup(self, id_organizacao, payload):
        return self.postrequest("/organizations/{}/policyObjects/groups".format(id_organizacao), payload)


def printa(jsonDado):
    print(json.dumps(jsonDado, indent=4, sort_keys=True))

if __name__ == '__main__':

    load_dotenv()
    meraki = MerakiAPI(os.environ.get("APIKEY"))

    payload_cidr = {"name": "TESTE2", "category": "network", "type": "cidr", "cidr":"10.0.0.0/24","groupIds":[]}
    payload_fqdn = {"name": "Teste URL", "category": "network", "type": "fqdn", "fqdn":"google.com","groupIds":[]}
    listaObjs = ['739153288842184442', '739153288842184437']
    payload_grupo = {"name": "Grupo via API", "category": "NetworkObjectGroup", "objectIds": listaObjs}
    
    organizacao = '739153288842183396'
    rede = 'L_739153288842210664'
    id_grupo_criado = '739153288842182896'
    printa(meraki.getPolicyObjects(organizacao))
    #printa(meraki.postPolicyObjGroup(organizacao, payload_grupo))

    #printa(meraki.createObject(organizacao, payload_ip))
    #printa(meraki.getOrganizacao(organizacao))
    #printa(meraki.getRedes(organizacao))
    #printa(meraki.getPolicyObjGroup(organizacao))
    #printa(meraki.getGroupPolicies(rede))
