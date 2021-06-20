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
        return self.__sessao.get(self.__baseURL+url, headers=self.__headers, data=self.__payload, timeout=5).json()

    def putrequest(self, url, payload): # Adicionar o exception
        return self.__sessao.put(self.__baseURL+url, headers=self.__headers, data=payload, timeout=5).json()

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
        return self.requesicao("/devices/{}/clients".format(serial_device))

    def getInterfaces(self, serial_device):
        return self.requesicao("/devices/{}/managementInterface".format(serial_device))

    def updateNetwork(self, id_rede, payload):
        return self.putrequest("/networks/{}/".format(id_rede), payload)

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

    idRede = 'L_566327653141843049'
    payload = meraki.getRede(idRede)
    print(payload)


