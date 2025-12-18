import random
from typing import List, Dict, Tuple
from Agente import Agente
from data_types import Observacao, Accao


class AgenteAprendizagem(Agente):
    def __init__(self, nome: str, accoes_possiveis: List[str]):
        super().__init__(nome)
        self.accoes_possiveis = accoes_possiveis
        self.q_table: Dict[Tuple[str, str], float] = {}

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        self.modo_teste = False

        self.estado_anterior = None
        self.accao_anterior = None
        self.ultimo_reward = 0.0
        self.estado_atual = None

    def cria(self, nome_do_ficheiro_parametros: str) -> 'Agente':
        return self

    def set_modo_teste(self, ativar: bool):
        self.modo_teste = ativar

    def observacao(self, obs: Observacao):
        self.estado_atual = str(obs.data)

    def avaliacaoEstadoAtual(self, recompensa: float):
        self.ultimo_reward = recompensa

    def age(self) -> Accao:
        if self.estado_anterior is not None and self.accao_anterior is not None and not self.modo_teste:
            self._aprender_q_learning()

        acao_escolhida = self._escolher_acao(self.estado_atual)

        self.estado_anterior = self.estado_atual
        self.accao_anterior = acao_escolhida

        return Accao(acao_escolhida)

    def _aprender_q_learning(self):
        chave_anterior = (self.estado_anterior, self.accao_anterior)
        q_antigo = self.q_table.get(chave_anterior, 0.0)

        max_q_atual = self._obter_max_q(self.estado_atual)

        novo_q = q_antigo + self.alpha * (self.ultimo_reward + (self.gamma * max_q_atual) - q_antigo)
        self.q_table[chave_anterior] = novo_q

    def _obter_max_q(self, estado: str) -> float:
        valores = [self.q_table.get((estado, a), 0.0) for a in self.accoes_possiveis]
        return max(valores) if valores else 0.0

    def _escolher_acao(self, estado: str) -> str:
        if self.modo_teste or random.random() > self.epsilon:
            q_values = {a: self.q_table.get((estado, a), 0.0) for a in self.accoes_possiveis}
            max_val = max(q_values.values())
            melhores_acoes = [a for a, q in q_values.items() if q == max_val]
            return random.choice(melhores_acoes)
        else:
            return random.choice(self.accoes_possiveis)