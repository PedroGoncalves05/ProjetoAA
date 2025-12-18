from typing import List, Union, Any
from Agente import Agente
from Ambiente import Ambiente
from AmbienteFarol import AmbienteFarol


class SimuladorMotor:
    def __init__(self):
        self.ambiente: Union[Ambiente, None] = None
        self.agentes: List[Agente] = []

    def criar_ambiente_farol(self):
        self.ambiente = AmbienteFarol(10, 10)

    def adicionar_agente(self, agente: Agente):
        self.agentes.append(agente)
        if isinstance(self.ambiente, AmbienteFarol):
            self.ambiente.adicionar_agente(agente)

    def executa(self, max_passos=100):
        if not self.ambiente or not self.agentes:
            print("Erro: Ambiente ou Agentes não inicializados.")
            return

        passo = 0
        simulacao_ativa = True
        print(f"A iniciar simulação com {len(self.agentes)} agente(s).")

        while simulacao_ativa and passo < max_passos:
            passo += 1

            self.ambiente.atualizacao()
            acoes_do_passo = {}

            for agente in self.agentes:
                obs = self.ambiente.observacaoPara(agente)
                agente.observacao(obs)
                acoes_do_passo[agente.nome] = agente.age()

            for agente in self.agentes:
                acao = acoes_do_passo[agente.nome]
                recompensa = self.ambiente.agir(acao, agente)
                agente.avaliacaoEstadoAtual(recompensa)

                if recompensa >= 100:
                    print(f"Agente {agente.nome} chegou ao Farol no passo {passo}!")
                    simulacao_ativa = False

        self.terminar_simulacao()

    def terminar_simulacao(self):
        print("Simulação terminada.")