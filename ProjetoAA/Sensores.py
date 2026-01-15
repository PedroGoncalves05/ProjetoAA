from Agente import Sensor
from data_types import Posicao, Observacao


class SensorFarol(Sensor):
    def __init__(self, ambiente):
        self.ambiente = ambiente

    def processa_observacao(self, pos_agente: Posicao) -> Observacao:
        farol = self.ambiente.posicao_farol
        if pos_agente == farol: return Observacao("Aqui")

        dx = farol.x - pos_agente.x
        dy = farol.y - pos_agente.y

        # Converte distância absoluta em direção relativa (reduz estados para a Q-Table)
        if abs(dx) > abs(dy):
            res = "Este" if dx > 0 else "Oeste"
        else:
            res = "Sul" if dy > 0 else "Norte"
        return Observacao(res)



class SensorLabirinto(Sensor):
    def __init__(self, ambiente):
        self.ambiente = ambiente

    def processa_observacao(self, pos_agente: Posicao) -> Observacao:
        # No labirinto, o ID do estado (y * largura + x) é o mais eficiente para a Q-Table
        id_estado = int(pos_agente.y * self.ambiente.largura + pos_agente.x)
        return Observacao(id_estado)