import random
from Ambiente import Ambiente
from Agente import Agente
from data_types import Observacao, Accao, Posicao


class AmbienteFarol(Ambiente):
    def __init__(self, largura=10, altura=10):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.posicoes_agentes = {}
        self.posicao_farol = None
        self.inicializar_estado("")

    def inicializar_estado(self, mapa_inicial: str):
        self.posicao_farol = Posicao(self.largura - 1, self.altura - 1)
        print(f"AmbienteFarol: Farol posicionado em {self.posicao_farol}")

    def adicionar_agente(self, agente: Agente):
        self.agentes.append(agente)

        self.posicoes_agentes[agente.nome] = Posicao(0, 0)

    def observacaoPara(self, agente: Agente) -> Observacao:
        pos_agente = self.posicoes_agentes[agente.nome]

        dx = self.posicao_farol.x - pos_agente.x
        dy = self.posicao_farol.y - pos_agente.y

        direcao = ""
        if dy > 0:
            direcao += "Norte"
        elif dy < 0:
            direcao += "Sul"

        if dx > 0:
            direcao += "Este"
        elif dx < 0:
            direcao += "Oeste"

        if direcao == "": direcao = "Aqui"

        return Observacao(direcao)

    def atualizacao(self):
        pass

    def agir(self, accao: Accao, agente: Agente) -> float:
        pos_atual = self.posicoes_agentes[agente.nome]
        distancia_anterior = pos_atual.distancia_euclidiana(self.posicao_farol)

        nova_pos = pos_atual.obter_nova_posicao(accao.tipo)

        if 0 <= nova_pos.x < self.largura and 0 <= nova_pos.y < self.altura:
            self.posicoes_agentes[agente.nome] = nova_pos
        else:
            nova_pos = pos_atual

        if nova_pos == self.posicao_farol:
            return 100.0


        distancia_nova = nova_pos.distancia_euclidiana(self.posicao_farol)
        shaping = (distancia_anterior - distancia_nova) * 10

        recompensa = shaping - 1.0

        return recompensa