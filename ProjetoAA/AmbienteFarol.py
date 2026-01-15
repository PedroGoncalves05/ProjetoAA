import math
from Ambiente import Ambiente
from Agente import Agente
from data_types import Accao, Posicao


class AmbienteFarol(Ambiente):
    def __init__(self):
        super().__init__()
        self.largura = 10
        self.altura = 10

        self.posicoes_agentes = {}
        self.posicao_farol = Posicao(9, 5)

        self.obstaculos = [
            Posicao(0, 5), Posicao(0, 6), Posicao(9, 3), Posicao(9, 4),
            Posicao(4, 0), Posicao(5, 0), Posicao(2, 9),
            Posicao(2, 2), Posicao(4, 4), Posicao(6, 2),
            Posicao(3, 7), Posicao(7, 5), Posicao(8, 1), Posicao(5, 8)
        ]

        self.angulo = 0
        self.velocidade_rotacao = 30  # Roda 30 graus
        self.frequencia_rotacao = 2
        self.contador_passos = 0

        self.cache_luz = set()
        self._calcular_feixe()

    def inicializar_estado(self, mapa_inicial: str = None):
        pass

    def atualizacao(self):
        pass

    def adicionar_agente(self, agente: Agente):
        if agente not in self.agentes:
            self.agentes.append(agente)
        self.posicoes_agentes[agente.nome] = Posicao(0, 0)

    def reiniciar_posicao_agente(self, agente: Agente):
        self.posicoes_agentes[agente.nome] = Posicao(0, 0)
        self.angulo = 0
        self.contador_passos = 0
        self._calcular_feixe()

    def observacaoPara(self, agente: Agente) -> int:
        p = self.posicoes_agentes[agente.nome]
        return p.y * self.largura + p.x

    def _calcular_feixe(self):
        self.cache_luz.clear()

        rad = math.radians(self.angulo)
        dx = math.cos(rad)
        dy = math.sin(rad)

        cx = self.posicao_farol.x + 0.5
        cy = self.posicao_farol.y + 0.5

        distancia = 0
        while True:
            cx += dx * 0.2
            cy += dy * 0.2
            distancia += 0.2

            ix = int(cx)
            iy = int(cy)

            if not (0 <= ix < self.largura and 0 <= iy < self.altura):
                break

            pos_teste = Posicao(ix, iy)
            if pos_teste in self.obstaculos:
                break

            if not (ix == self.posicao_farol.x and iy == self.posicao_farol.y):
                self.cache_luz.add((ix, iy))

            if distancia > 20: break

    def _esta_iluminado(self, pos: Posicao) -> bool:
        return (pos.x, pos.y) in self.cache_luz

    def agir(self, accao, agente):
        pos_atual = self.posicoes_agentes[agente.nome]
        dist_anterior = pos_atual.distancia_euclidiana(self.posicao_farol)
        tipo = accao.tipo if hasattr(accao, 'tipo') else accao

        nova_pos = pos_atual.obter_nova_posicao(tipo)

        nx = max(0, min(nova_pos.x, self.largura - 1))
        ny = max(0, min(nova_pos.y, self.altura - 1))
        pos_tentativa = Posicao(nx, ny)

        if pos_tentativa in self.obstaculos:
            return -0.5

        pos_atual.x = nx
        pos_atual.y = ny
        dist_nova = pos_atual.distancia_euclidiana(self.posicao_farol)
        recompensa_shaping = (dist_anterior - dist_nova) * 5.0
        reward_luz = 2.0 if self._esta_iluminado(pos_atual) else 0.0

        if pos_atual == self.posicao_farol:
            return 100.0 + reward_luz

        return recompensa_shaping + reward_luz - 0.1  # Penalização por passo