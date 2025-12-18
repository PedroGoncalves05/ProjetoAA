from typing import Dict, Any
import math

class Posicao:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Posicao):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return f"({self.x}, {self.y})"

    def distancia_euclidiana(self, outra_pos: 'Posicao') -> float:
        return math.sqrt((self.x - outra_pos.x)**2 + (self.y - outra_pos.y)**2)

    def obter_nova_posicao(self, direcao: str) -> 'Posicao':
        dx, dy = 0, 0
        if direcao == "Norte": dy = 1
        elif direcao == "Sul": dy = -1
        elif direcao == "Este": dx = 1
        elif direcao == "Oeste": dx = -1
        return Posicao(self.x + dx, self.y + dy)

class Observacao:
    def __init__(self, data: Any):
        self.data = data

class Accao:
    def __init__(self, tipo: str, parametros: Dict[str, Any] = None):
        self.tipo = tipo
        self.parametros = parametros if parametros is not None else {}