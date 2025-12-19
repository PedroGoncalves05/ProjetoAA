import numpy as np
import random
from Agente import Agente


class AgenteAprendizagem(Agente):
    def __init__(self, nome, accoes):
        super().__init__(nome)
        self.accoes = accoes
        self.num_accoes = len(accoes)

        # --- HIPERPARÂMETROS ---
        self.alpha = 0.5  # Taxa de aprendizagem
        self.gamma = 0.95  # Fator de desconto
        self.epsilon = 1.0  # Exploração inicial (100%)

        # --- MEMÓRIA (Q-TABLE) ---
        # 100 estados x N Ações
        self.q_table = np.zeros((100, self.num_accoes))

        # Variáveis temporárias para o ciclo de aprendizagem
        self.estado_anterior_id = None
        self.accao_anterior_idx = None
        self.recompensa_anterior = 0

    def cria(self):
        return AgenteAprendizagem(self.nome, self.accoes)

    def set_modo_teste(self, ativar: bool):
        """ Desativa a exploração (epsilon=0) para a demo final """
        if ativar:
            self.epsilon = 0.0
            print(f"Modo Teste ATIVADO para {self.nome} (Epsilon=0)")
        else:
            self.epsilon = 1.0

    def observacao(self, estado_id):
        """
        Recebe o novo estado, converte para INT com segurança e aprende.
        """
        # --- CONVERSÃO SEGURA (Resolve erros de tipo) ---
        try:
            novo_estado_id = int(estado_id)
        except (TypeError, ValueError):
            try:
                novo_estado_id = int(str(estado_id))
            except:
                novo_estado_id = 0  # Fallback

        # --- APRENDIZAGEM (Q-LEARNING STANDARD) ---
        if (self.estado_anterior_id is not None) and (self.accao_anterior_idx is not None):
            s = self.estado_anterior_id
            a = self.accao_anterior_idx
            r = self.recompensa_anterior
            s_prime = novo_estado_id

            # Verificar limites da tabela
            if s < len(self.q_table) and s_prime < len(self.q_table):
                q_antigo = self.q_table[s, a]
                max_q_futuro = np.max(self.q_table[s_prime, :])

                # Equação de Bellman
                novo_q = q_antigo + self.alpha * (r + (self.gamma * max_q_futuro) - q_antigo)
                self.q_table[s, a] = novo_q

        # Atualizar memória
        self.estado_anterior_id = novo_estado_id

    def age(self):
        """ Escolhe a ação (Epsilon-Greedy) """
        estado_atual = self.estado_anterior_id

        if estado_atual is None or estado_atual >= len(self.q_table):
            estado_atual = 0

        # Exploração
        if random.random() < self.epsilon:
            acao_idx = random.randint(0, self.num_accoes - 1)
        # Aproveitamento
        else:
            valores_q = self.q_table[estado_atual, :]
            # Pequeno ruído para desempatar zeros
            acao_idx = np.argmax(valores_q + np.random.randn(1, self.num_accoes) * 0.001)

        self.accao_anterior_idx = acao_idx
        return self.accoes[acao_idx]

    def avaliacaoEstadoAtual(self, recompensa):
        """ Recebe a recompensa e aprende se for o fim do episódio """
        self.recompensa_anterior = recompensa

        # Se for estado terminal (vitória/derrota), aprende já
        if abs(recompensa) > 10:
            s = self.estado_anterior_id
            a = self.accao_anterior_idx
            if s is not None and a is not None and s < len(self.q_table):
                q_antigo = self.q_table[s, a]
                # Sem max_q_futuro porque o jogo acabou
                novo_q = q_antigo + self.alpha * (recompensa - q_antigo)
                self.q_table[s, a] = novo_q