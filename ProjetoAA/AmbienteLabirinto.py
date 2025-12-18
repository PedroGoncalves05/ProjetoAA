from Ambiente import Ambiente
from Agente import Agente
from data_types import Observacao, Accao, Posicao
import random


class AmbienteLabirinto(Ambiente):
    def __init__(self):
        super().__init__()
        self.grelha = [
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 1, 1, 0]
        ]
        self.largura = 10
        self.altura = 10
        self.posicao_final = Posicao(9, 9)
        self.posicoes_agentes = {}

    def inicializar_estado(self, mapa_inicial: str):
        pass

    def adicionar_agente(self, agente: Agente):
        self.agentes.append(agente)
        self.posicoes_agentes[agente.nome] = Posicao(0, 0)

    def observacaoPara(self, agente: Agente) -> Observacao:
        pos = self.posicoes_agentes[agente.nome]



        obs_str = f"{pos.x},{pos.y}"

        return Observacao(obs_str)

    def atualizacao(self):
        pass

    def agir(self, accao: Accao, agente: Agente) -> float:
        pos_atual = self.posicoes_agentes[agente.nome]
        nova_pos = pos_atual.obter_nova_posicao(accao.tipo)

        bateu = False
        if not (0 <= nova_pos.x < self.largura and 0 <= nova_pos.y < self.altura):
            bateu = True
        elif self.grelha[nova_pos.y][nova_pos.x] == 1:
            bateu = True

        if bateu:
            return -5.0


        self.posicoes_agentes[agente.nome] = nova_pos


        if nova_pos == self.posicao_final:
            return 100.0

        return -1.0