import matplotlib.pyplot as plt
import time
import sys
import numpy as np

from AgenteAprendizagem import AgenteAprendizagem
from AmbienteFarol import AmbienteFarol
from AmbienteLabirinto import AmbienteLabirinto
from data_types import Posicao

# Importação das classes dos Sensores (deves ter o ficheiro Sensores.py) [cite: 431]
from Sensores import SensorFarol, SensorLabirinto

try:
    from VisualizadorGUI import VisualizadorGUI
except ImportError:
    VisualizadorGUI = None
    print("Aviso: VisualizadorGUI não encontrado.")

# Configurações globais
NUM_EPISODIOS_TREINO = 2000  # Aumentado para dar tempo ao Novelty de explorar
MAX_PASSOS_POR_EPISODIO = 500
FATOR_EXPLORACAO_INICIAL = 1.0
INTERVALO_RELATORIO = 100


def rodar_episodio(agente, ambiente, gui=None, mapa_calor=None):
    if hasattr(ambiente, 'reiniciar_posicao_agente'):
        ambiente.reiniciar_posicao_agente(agente)
    elif agente not in ambiente.agentes:
        ambiente.adicionar_agente(agente)

    # Reset de estado interno do agente para o novo episódio [cite: 429]
    agente.estado_anterior_id = None
    agente.accao_anterior_idx = None

    passos = 0
    recompensa_total = 0
    terminou = False

    while not terminou and passos < MAX_PASSOS_POR_EPISODIO:
        passos += 1

        # Obtenção da posição bruta para o processamento do sensor [cite: 424, 461]
        pos_bruta = ambiente.posicoes_agentes[agente.nome]
        agente.observacao(pos_bruta)

        acao = agente.age()
        recompensa = ambiente.agir(acao, agente)
        recompensa_total += recompensa

        # Atualização do heatmap para análise de desempenho [cite: 391, 481]
        if mapa_calor is not None:
            pos = ambiente.posicoes_agentes[agente.nome]
            if 0 <= pos.y < len(mapa_calor) and 0 <= pos.x < len(mapa_calor[0]):
                mapa_calor[pos.y][pos.x] += 1

        agente.avaliacaoEstadoAtual(recompensa)

        if gui:
            gui.desenhar_ambiente(ambiente, agente)
            time.sleep(0.01)

        # Verificação de sucesso (chegada ao objetivo) [cite: 447, 463]
        pos_atual = ambiente.posicoes_agentes[agente.nome]
        destino = getattr(ambiente, 'posicao_final', None) or getattr(ambiente, 'posicao_farol', None)

        if destino and pos_atual == destino:
            terminou = True

    return passos, recompensa_total


def desenhar_graficos(hist_passos, hist_rewards, titulo):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Gráfico de Passos (Curva de Aprendizagem)
    ax1.plot(hist_passos, color='#ADD8E6', alpha=0.6, label='Passos Realizados')
    janela = 50
    if len(hist_passos) > janela:
        media = np.convolve(hist_passos, np.ones(janela) / janela, mode='valid')
        ax1.plot(range(janela - 1, len(hist_passos)), media, color='blue', linewidth=2, label='Média Móvel')
    ax1.set_title(f"Curva de Aprendizagem - {titulo}")
    ax1.legend()

    # Gráfico de Recompensa [cite: 393, 414]
    ax2.plot(hist_rewards, color='#FA8072', alpha=0.6, label='Recompensa Total')
    if len(hist_rewards) > janela:
        media_r = np.convolve(hist_rewards, np.ones(janela) / janela, mode='valid')
        ax2.plot(range(janela - 1, len(hist_rewards)), media_r, color='red', linewidth=2, label='Média Móvel')
    ax2.set_title(f"Evolução da Recompensa - {titulo}")
    ax2.legend()
    plt.tight_layout()
    plt.show()


def main():
    print("=== SIMULADOR SMA ===")
    print("1. Q-Learning (Otimização)")
    print("2. Novelty Search (Exploração)")
    op_algo = input("Escolha o Algoritmo (1/2): ").strip()
    nome_algo = "NOVELTY" if op_algo == '2' else "QLEARNING"

    print("\n1. Ambiente Farol")
    print("2. Ambiente Labirinto")
    op_amb = input("Escolha o Ambiente (1/2): ").strip()

    # Inicialização do Ambiente e Sensor correspondente [cite: 410, 431]
    if op_amb == '2':
        amb = AmbienteLabirinto()
        nome_prob = "Labirinto"
        sensor = SensorLabirinto(amb)
        if hasattr(amb, 'set_modo_novelty'):
            amb.set_modo_novelty(nome_algo == "NOVELTY")
    else:
        amb = AmbienteFarol()
        nome_prob = "Farol"
        sensor = SensorFarol(amb)

    print(f"\n--- TREINO: {nome_prob} | ALGORITMO: {nome_algo} ---")

    agente = AgenteAprendizagem("Robo", ["Norte", "Sul", "Este", "Oeste"])
    agente.instala(sensor)  # Instalação modular do sensor [cite: 431]
    agente.epsilon = FATOR_EXPLORACAO_INICIAL

    h, w = getattr(amb, 'altura', 10), getattr(amb, 'largura', 10)
    mapa_visitas = np.zeros((h, w))
    historico_p, historico_r = [], []

    for i in range(NUM_EPISODIOS_TREINO):
        # Ajuste de Exploração (Epsilon): Mais persistente no Novelty Search
        if nome_algo == "NOVELTY":
            # Mantém a exploração ativa por mais tempo para descobrir o mapa
            agente.epsilon = max(0.2, agente.epsilon * 0.9995)
        else:
            # Foca-se mais rápido no caminho ótimo
            agente.epsilon = max(0.05, agente.epsilon * 0.998)

        p, r = rodar_episodio(agente, amb, gui=None, mapa_calor=mapa_visitas)
        historico_p.append(p)
        historico_r.append(r)

        if (i + 1) % INTERVALO_RELATORIO == 0:
            print(f"Ep {i + 1}: Passos={p} | Rec={r:.1f} | Epsilon={agente.epsilon:.2f}")

    desenhar_graficos(historico_p, historico_r, nome_prob)

    if VisualizadorGUI:
        print("\n--- MODO DE TESTE (Visualização) ---")
        input("Pressione Enter para iniciar...")
        agente.set_modo_teste(True)  # Ativa política fixa aprendida [cite: 482]
        amb.reiniciar_posicao_agente(agente)
        gui = VisualizadorGUI(largura_grelha=amb.largura, altura_grelha=amb.altura)

        try:
            rodar_episodio(agente, amb, gui=gui)
            print("Simulação terminada.")
            input("Pressione Enter para fechar...")
        except Exception as e:
            print(f"Erro na visualização: {e}")
        finally:
            gui.fechar()


if __name__ == "__main__":
    main()