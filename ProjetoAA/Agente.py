from abc import ABC, abstractmethod
from typing import List, Any
from data_types import Observacao, Accao

class Sensor(ABC):
    @abstractmethod
    def processa_observacao(self, obs_bruta: Any) -> Observacao:
        pass

class Agente(ABC):
    def __init__(self, nome: str):
        self.nome = nome
        self.sensores: List[Sensor] = []

    @abstractmethod
    def cria(self, nome_do_ficheiro_parametros: str) -> 'Agente':
        pass

    @abstractmethod
    def observacao(self, obs: Observacao):
        pass

    @abstractmethod
    def age(self) -> Accao:
        pass

    @abstractmethod
    def avaliacaoEstadoAtual(self, recompensa: float):
        pass

    def instala(self, sensor: Sensor):
        self.sensores.append(sensor)

    def comunica(self, mensagem: str, de_agente: 'Agente'):
        pass