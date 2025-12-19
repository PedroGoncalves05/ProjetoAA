import numpy as np
import random
from Agente import Agente


class AgenteAprendizagem(Agente):
    def __init__(self, nome, accoes):
        super().__init__(nome)
        self.accoes = accoes
        self.num_accoes = len(accoes)

        # --- HIPERPARÂMETROS ---
        self.alpha = 0.5
        self.gamma = 0.95
        self.epsilon = 1.0

        self.q_table = np.zeros((100, self.num_accoes))

        self.estado_anterior_id = None
        self.accao_anterior_idx = None
        self.recompensa_anterior = 0

    def cria(self):
        return AgenteAprendizagem(self.nome, self.accoes)

    def set_modo_teste(self, ativar: bool):
        if ativar:
            self.epsilon = 0.0
            print(f"Modo Teste ATIVADO para {self.nome} (Epsilon=0)")
        else:
            self.epsilon = 1.0

    def observacao(self, estado_id):
        try:
            novo_estado_id = int(estado_id)
        except (TypeError, ValueError):
            try:
                novo_estado_id = int(str(estado_id))
            except:
                novo_estado_id = 0  # Fallback

        if (self.estado_anterior_id is not None) and (self.accao_anterior_idx is not None):
            s = self.estado_anterior_id
            a = self.accao_anterior_idx
            r = self.recompensa_anterior
            s_prime = novo_estado_id

            if s < len(self.q_table) and s_prime < len(self.q_table):
                q_antigo = self.q_table[s, a]
                max_q_futuro = np.max(self.q_table[s_prime, :])

                novo_q = q_antigo + self.alpha * (r + (self.gamma * max_q_futuro) - q_antigo)
                self.q_table[s, a] = novo_q

        self.estado_anterior_id = novo_estado_id

    def age(self):
        estado_atual = self.estado_anterior_id

        if estado_atual is None or estado_atual >= len(self.q_table):
            estado_atual = 0

        if random.random() < self.epsilon:
            acao_idx = random.randint(0, self.num_accoes - 1)
        else:
            valores_q = self.q_table[estado_atual, :]
            acao_idx = np.argmax(valores_q + np.random.randn(1, self.num_accoes) * 0.001)

        self.accao_anterior_idx = acao_idx
        return self.accoes[acao_idx]

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_anterior = recompensa

        if abs(recompensa) > 10:
            s = self.estado_anterior_id
            a = self.accao_anterior_idx
            if s is not None and a is not None and s < len(self.q_table):
                q_antigo = self.q_table[s, a]
                novo_q = q_antigo + self.alpha * (recompensa - q_antigo)
                self.q_table[s, a] = novo_q