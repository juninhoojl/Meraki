# Procedimento contencao

from abc import ABC, abstractmethod


class ObjRede(ABC):
    def __init__(self, task):
        self.__task = task
        self.__category = 'network'


payload_fqdn = {"name": "Teste URL", "category": "network", "type": "fqdn", "fqdn":"google.com","groupIds":[]}