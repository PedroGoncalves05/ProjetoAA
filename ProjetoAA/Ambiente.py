from abc import ABC, abstractmethod
from typing import List, Any
from data_types import Observacao, Accao
from Agente import Agente

class Ambiente(ABC):
    def __init__(self, agentes: List[Agente] = None):
        self.agentes = agentes if agentes is not None else []
        self.estado_atual: Any = None

    @abstractmethod
    def observacaoPara(self, agente: Agente) -> Observacao:
        pass

    @abstractmethod
    def atualizacao(self):
        pass

    @abstractmethod
    def agir(self, accao: Accao, agente: Agente) -> float:
        pass

    @abstractmethod
    def inicializar_estado(self, mapa_inicial: str):
        pass