import random
from typing import List
from Agente import Agente
from data_types import Observacao, Accao

class AgenteFixo(Agente):
    def __init__(self, nome: str, accoes_possiveis: List[str]):
        super().__init__(nome)
        self.accoes_possiveis = accoes_possiveis
        self.ultima_observacao = None

    def cria(self, nome_do_ficheiro_parametros: str) -> 'Agente':
        return AgenteFixo(self.nome, ["Norte", "Sul", "Este", "Oeste"])

    def observacao(self, obs: Observacao):
        self.ultima_observacao = obs

    def age(self) -> Accao:
        tipo_accao = random.choice(self.accoes_possiveis)
        return Accao(tipo_accao)

    def avaliacaoEstadoAtual(self, recompensa: float):
        pass