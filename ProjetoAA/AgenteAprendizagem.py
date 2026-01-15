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
        # Aumentamos o tamanho da tabela para acomodar novos estados combinados
        self.q_table = np.zeros((2000, self.num_accoes))

        self.estado_anterior_id = None
        self.accao_anterior_idx = None
        self.recompensa_anterior = 0

    def set_modo_teste(self, ativar: bool):
        self.epsilon = 0.0 if ativar else 1.0

    def observacao(self, obs_vinda_do_main):
        # 1. Chama a lógica base para usar o sensor
        super().observacao(obs_vinda_do_main)

        # 2. Extração de dados da Observacao (Dicionário vindo dos novos sensores)
        data = self.ultima_observacao.data if self.ultima_observacao else 0
        novo_estado_id = 0

        # 3. Lógica de Mapeamento de Estados baseada no novo formato dos sensores
        if isinstance(data, dict):
            # CASO LABIRINTO: Usa o ID da célula fornecido pelo sensor
            if "id" in data:
                novo_estado_id = int(data["id"])

            # CASO FAROL: Combina Direção + Luz num único ID de estado
            elif "direcao" in data:
                mapeamento_dir = {"Norte": 0, "Sul": 1, "Este": 2, "Oeste": 3, "Aqui": 4}
                dir_id = mapeamento_dir.get(data["direcao"], 0)
                luz_id = 1 if data.get("luz", False) else 0
                # Cria um ID único combinando os dois: ex: Norte+Sombra=0, Norte+Luz=5
                novo_estado_id = dir_id + (luz_id * 5)
        else:
            # Fallback para compatibilidade com IDs numéricos diretos
            try:
                novo_estado_id = int(data)
            except:
                novo_estado_id = 0

        # 4. Atualização Q-Learning [cite: 480]
        if (self.estado_anterior_id is not None) and (self.accao_anterior_idx is not None):
            s, a, r = self.estado_anterior_id, self.accao_anterior_idx, self.recompensa_anterior
            s_prime = novo_estado_id

            q_antigo = self.q_table[s, a]
            max_q_futuro = np.max(self.q_table[s_prime, :])
            self.q_table[s, a] = q_antigo + self.alpha * (r + (self.gamma * max_q_futuro) - q_antigo)

        self.estado_anterior_id = novo_estado_id

    def age(self):
        s = self.estado_anterior_id if self.estado_anterior_id is not None else 0
        # Estratégia Epsilon-Greedy
        if random.random() < self.epsilon:
            idx = random.randint(0, self.num_accoes - 1)
        else:
            # Exploração com ruído para desempate
            idx = np.argmax(self.q_table[s, :] + np.random.randn(1, self.num_accoes) * 0.001)

        self.accao_anterior_idx = idx
        return self.accoes[idx]

    def avaliacaoEstadoAtual(self, recompensa):
        self.recompensa_anterior = recompensa