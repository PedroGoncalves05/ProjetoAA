from Ambiente import Ambiente
from Agente import Agente
from data_types import Accao, Posicao
import numpy as np


class AmbienteLabirinto(Ambiente):
    def __init__(self):
        super().__init__()
        # 1 = Parede, 0 = Livre
        # MAPA ORIGINAL (Complexo)
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

        # Mapa de visitas (Novelty)
        self.mapa_visitas = np.zeros((self.altura, self.largura))
        self.modo_novelty = False

    def inicializar_estado(self, mapa_inicial: str = None):
        pass

    def atualizacao(self):
        pass

    def set_modo_novelty(self, ativo: bool):
        self.modo_novelty = ativo
        if ativo:
            self.mapa_visitas = np.zeros((self.altura, self.largura))

    def adicionar_agente(self, agente: Agente):
        if agente not in self.agentes:
            self.agentes.append(agente)
        self.posicoes_agentes[agente.nome] = Posicao(0, 0)

    def reiniciar_posicao_agente(self, agente: Agente):
        self.posicoes_agentes[agente.nome] = Posicao(0, 0)

    def observacaoPara(self, agente: Agente) -> int:
        pos = self.posicoes_agentes[agente.nome]
        return int(pos.y * self.largura + pos.x)

    def agir(self, accao: Accao, agente: Agente) -> float:
        pos_atual = self.posicoes_agentes[agente.nome]

        tipo = accao.tipo if hasattr(accao, 'tipo') else accao
        move_x, move_y = 0, 0

        if tipo == "Norte" or tipo == 0:
            move_y = -1
        elif tipo == "Sul" or tipo == 1:
            move_y = 1
        elif tipo == "Este" or tipo == 2:
            move_x = 1
        elif tipo == "Oeste" or tipo == 3:
            move_x = -1

        novo_x = pos_atual.x + move_x
        novo_y = pos_atual.y + move_y

        bateu = False
        recompensa = 0.0

        if not (0 <= novo_x < self.largura and 0 <= novo_y < self.altura):
            bateu = True
        elif self.grelha[novo_y][novo_x] == 1:
            bateu = True

        if bateu:
            novo_x, novo_y = pos_atual.x, pos_atual.y
            recompensa = -0.5  # Penalidade por bater
        else:
            self.posicoes_agentes[agente.nome] = Posicao(novo_x, novo_y)
            self.mapa_visitas[novo_y][novo_x] += 1

            if self.modo_novelty:
                n_visitas = self.mapa_visitas[novo_y][novo_x]
                recompensa = 10.0 / n_visitas
                if novo_x == self.posicao_final.x and novo_y == self.posicao_final.y:
                    recompensa += 20.0
            else:
                # Q-Learning Puro
                recompensa = -0.1  # Custo por passo

                if novo_x == self.posicao_final.x and novo_y == self.posicao_final.y:
                    recompensa = 100.0

        return recompensa