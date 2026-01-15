from Agente import Sensor
from data_types import Posicao, Observacao


class SensorFarol(Sensor):
    def __init__(self, ambiente):
        self.ambiente = ambiente

    def processa_observacao(self, pos_agente: Posicao) -> Observacao:
        farol = self.ambiente.posicao_farol

        if pos_agente == farol:
            return Observacao("Aqui")

        dx = farol.x - pos_agente.x
        dy = farol.y - pos_agente.y

        if abs(dx) > abs(dy):
            direcao = "Este" if dx > 0 else "Oeste"
        else:
            direcao = "Sul" if dy > 0 else "Norte"

        iluminado = self.ambiente._esta_iluminado(pos_agente)

        return Observacao({"direcao": direcao, "luz": iluminado})


class SensorLabirinto(Sensor):
    """
    Implementa a percepção limitada (grelha de adjacência). [cite: 146, 504]
    O agente apenas vê se as células vizinhas estão livres ou se são paredes.
    """

    def __init__(self, ambiente):
        self.ambiente = ambiente

    def processa_observacao(self, pos_agente: Posicao) -> Observacao:
        # Define as direções a observar (Norte, Sul, Este, Oeste)
        direcoes = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "O": (-1, 0)
        }

        percepcao_local = {}

        for nome, (dx, dy) in direcoes.items():
            nx, ny = pos_agente.x + dx, pos_agente.y + dy

            # Verifica limites do mapa e obstáculos [cite: 422]
            if not (0 <= nx < self.ambiente.largura and 0 <= ny < self.ambiente.altura):
                percepcao_local[nome] = "Parede"
            elif self.ambiente.grelha[ny][nx] == 1:
                percepcao_local[nome] = "Parede"
            else:
                percepcao_local[nome] = "Livre"

        # O estado para a Q-Table pode ser a combinação destas paredes + ID da célula
        # para garantir que o agente sabe onde está mas com visão limitada.
        id_celula = int(pos_agente.y * self.ambiente.largura + pos_agente.x)

        return Observacao({
            "id": id_celula,
            "vizinhos": percepcao_local
        })