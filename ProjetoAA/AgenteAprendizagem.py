import numpy as np
import random
from Agente import Agente


class AgenteAprendizagem(Agente):
    def __init__(self, nome, accoes):
        super().__init__(nome)
        self.accoes = accoes
        self.num_accoes = len(accoes)
        self.alpha = 0.5
        self.gamma = 0.95
        self.epsilon = 1.0
        self.q_table = np.zeros((1000, self.num_accoes))

        self.estado_anterior_id = None
        self.accao_anterior_idx = None
        self.recompensa_anterior = 0

    def set_modo_teste(self, ativar: bool):
        # Define epsilon como 0 para usar apenas o conhecimento adquirido no modo teste
        self.epsilon = 0.0 if ativar else 1.0

    def observacao(self, obs_vinda_do_main):
        # 1. Chama a lógica base para usar o sensor
        super().observacao(obs_vinda_do_main)

        # 2. Extrai os dados (evita erro se ultima_observacao for None)
        if self.ultima_observacao and hasattr(self.ultima_observacao, 'data'):
            data = self.ultima_observacao.data
        else:
            data = 0

        # 3. Mapear strings para IDs numéricos (Ambiente Farol)
        mapeamento_farol = {"Norte": 0, "Sul": 1, "Este": 2, "Oeste": 3, "Aqui": 4}
        if data in mapeamento_farol:
            novo_estado_id = mapeamento_farol[data]
        else:
            try:
                novo_estado_id = int(data)
            except:
                novo_estado_id = 0

        # 4. Atualização Q-Learning
        if (self.estado_anterior_id is not None) and (self.accao_anterior_idx is not None):
            s, a, r = self.estado_anterior_id, self.accao_anterior_idx, self.recompensa_anterior
            s_prime = novo_estado_id

            q_antigo = self.q_table[s, a]
            max_q_futuro = np.max(self.q_table[s_prime, :])
            self.q_table[s, a] = q_antigo + self.alpha * (r + (self.gamma * max_q_futuro) - q_antigo)

        self.estado_anterior_id = novo_estado_id

    def age(self):
        s = self.estado_anterior_id if self.estado_anterior_id is not None else 0
        if random.random() < self.epsilon:
            idx = random.randint(0, self.num_accoes - 1)
        else:
            idx = np.argmax(self.q_table[s, :] + np.random.randn(1, self.num_accoes) * 0.001)

        self.accao_anterior_idx = idx
        return self.accoes[idx]

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_anterior = recompensa