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


        self.obstaculos = [
            Posicao(0, 5), Posicao(0, 6), Posicao(9, 3), Posicao(9, 4),
            Posicao(4, 0), Posicao(5, 0), Posicao(2, 9),
            Posicao(2, 2), Posicao(4, 4), Posicao(6, 2),
            Posicao(3, 7), Posicao(7, 5), Posicao(8, 1), Posicao(5, 8)
        ]
        self.inicializar_estado("")

    def inicializar_estado(self, mapa_inicial: str):
        self.posicao_farol = Posicao(self.largura - 1, self.altura - 1)

    def atualizacao(self):

        pass

    def adicionar_agente(self, agente: Agente):
        self.agentes.append(agente)
        self.posicoes_agentes[agente.nome] = Posicao(0, 0)

    def observacaoPara(self, agente: Agente) -> Observacao:
        pos_agente = self.posicoes_agentes[agente.nome]


        dx = self.posicao_farol.x - pos_agente.x
        dy = self.posicao_farol.y - pos_agente.y
        dir_farol = ""
        if dy > 0:
            dir_farol += "N"
        elif dy < 0:
            dir_farol += "S"
        if dx > 0:
            dir_farol += "E"
        elif dx < 0:
            dir_farol += "O"
        if dir_farol == "": dir_farol = "Aqui"


        obs_proximidade = ""
        for d_nome in ["Norte", "Sul", "Este", "Oeste"]:
            p_teste = pos_agente.obter_nova_posicao(d_nome)

            if not (0 <= p_teste.x < self.largura and 0 <= p_teste.y < self.altura) or \
                    any(obs.x == p_teste.x and obs.y == p_teste.y for obs in self.obstaculos):
                obs_proximidade += "1"
            else:
                obs_proximidade += "0"


        return Observacao(f"{dir_farol}_{obs_proximidade}")

    def agir(self, accao: Accao, agente: Agente) -> float:
        pos_atual = self.posicoes_agentes[agente.nome]
        dist_anterior = pos_atual.distancia_euclidiana(self.posicao_farol)
        nova_pos = pos_atual.obter_nova_posicao(accao.tipo)


        fora_limites = not (0 <= nova_pos.x < self.largura and 0 <= nova_pos.y < self.altura)
        e_obstaculo = any(obs.x == nova_pos.x and obs.y == nova_pos.y for obs in self.obstaculos)

        if fora_limites or e_obstaculo:
            return -2.0

        self.posicoes_agentes[agente.nome] = nova_pos

        if nova_pos == self.posicao_farol:
            return 100.0

        dist_nova = nova_pos.distancia_euclidiana(self.posicao_farol)
        shaping = (dist_anterior - dist_nova) * 10
        return shaping - 1.0