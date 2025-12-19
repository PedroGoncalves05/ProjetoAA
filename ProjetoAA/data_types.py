import math
from typing import Dict, Any

class Posicao:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Permite comparar se duas posições são iguais (p1 == p2)."""
        return isinstance(other, Posicao) and self.x == other.x and self.y == other.y

    def __hash__(self):
        """Permite usar Posicao como chave em dicionários."""
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def distancia_euclidiana(self, outra_pos: 'Posicao') -> float:
        """Calcula a distância em linha reta."""
        return math.sqrt((self.x - outra_pos.x)**2 + (self.y - outra_pos.y)**2)

    def obter_nova_posicao(self, direcao: str) -> 'Posicao':
        """
        Retorna uma NOVA posição baseada na direção.
        Sistema de Matriz: (0,0) é canto superior esquerdo.
        Norte diminui Y, Sul aumenta Y.
        """
        nx, ny = self.x, self.y
        if direcao == "Norte":
            ny -= 1
        elif direcao == "Sul":
            ny += 1
        elif direcao == "Este":
            nx += 1
        elif direcao == "Oeste":
            nx -= 1
        return Posicao(nx, ny)

class Observacao:
    def __init__(self, data: Any):
        self.data = data

class Accao:
    def __init__(self, tipo: str, parametros: Dict[str, Any] = None):
        self.tipo = tipo
        self.parametros = parametros if parametros is not None else {}