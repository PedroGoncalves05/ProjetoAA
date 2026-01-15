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
        self.ultima_observacao = None

    def instala(self, sensor: Sensor):
        self.sensores.append(sensor)

    def observacao(self, obs_bruta: Any):
        if self.sensores:
            # O sensor transforma a posição bruta numa Observação útil
            self.ultima_observacao = self.sensores[0].processa_observacao(obs_bruta)
        else:
            self.ultima_observacao = obs_bruta

    @abstractmethod
    def age(self) -> Accao:
        pass

    @abstractmethod
    def avaliacaoEstadoAtual(self, recompensa: float):
        pass