import matplotlib.pyplot as plt
import time
import sys

# Importações do projeto
from AgenteAprendizagem import AgenteAprendizagem
from AmbienteFarol import AmbienteFarol
from AmbienteLabirinto import AmbienteLabirinto
from VisualizadorGUI import VisualizadorGUI

# --- Configurações ---
NUM_EPISODIOS_TREINO = 1000  # Aumentei para dar tempo de ver a evolução
MAX_PASSOS_POR_EPISODIO = 100
FATOR_EXPLORACAO = 0.2
INTERVALO_RELATORIO = 50  # Atualiza a tabela a cada 50 episódios


def rodar_episodio(agente, ambiente, gui=None):
    """
    Executa um episódio e retorna (passos, recompensa, sucesso).
    """
    ambiente.posicoes_agentes = {}
    ambiente.adicionar_agente(agente)
    agente.estado_anterior = None
    agente.accao_anterior = None

    passos = 0
    recompensa_total = 0
    terminou = False
    sucesso = False

    while not terminou and passos < MAX_PASSOS_POR_EPISODIO:
        passos += 1

        obs = ambiente.observacaoPara(agente)
        agente.observacao(obs)
        acao = agente.age()
        recompensa = ambiente.agir(acao, agente)

        recompensa_total += recompensa
        agente.avaliacaoEstadoAtual(recompensa)

        if gui:
            gui.desenhar_ambiente(ambiente, agente)
            time.sleep(0.05)

        if recompensa >= 90:
            terminou = True
            sucesso = True

    return passos, recompensa_total, sucesso


def desenhar_barra_progresso(percentagem, largura=30):
    preenchido = int(largura * percentagem)
    barra = '█' * preenchido + '-' * (largura - preenchido)
    sys.stdout.write(f"\rProgresso: |{barra}| {int(percentagem * 100)}% ")
    sys.stdout.flush()


def main():
    print("\n=== SIMULADOR DE SISTEMAS MULTI-AGENTE ===")
    print("1. Problema do Farol")
    print("2. Problema do Labirinto")
    escolha = input("Escolha o cenário (1 ou 2): ")

    if escolha == '2':
        ambiente_classe = AmbienteLabirinto
        nome_prob = "Labirinto"
    else:
        ambiente_classe = AmbienteFarol
        nome_prob = "Farol"

    print(f"\n--- INICIANDO TREINO: {nome_prob} ({NUM_EPISODIOS_TREINO} Eps) ---")


    accoes = ["Norte", "Sul", "Este", "Oeste"]
    agente = AgenteAprendizagem("Robo1", accoes)
    agente.epsilon = FATOR_EXPLORACAO

    historico_passos = []

    soma_passos = 0
    soma_reward = 0
    sucessos_lote = 0


    print("-" * 85)
    print(
        f"| {'Lote (Episódios)':^18} | {'Passos (Média)':^15} | {'Reward (Média)':^15} | {'Sucesso %':^10} | {'Epsilon':^8} |")
    print("-" * 85)

    tempo_inicio = time.time()

    for i in range(1, NUM_EPISODIOS_TREINO + 1):
        amb = ambiente_classe()
        passos, recompensa, sucesso = rodar_episodio(agente, amb, gui=None)

        historico_passos.append(passos)


        soma_passos += passos
        soma_reward += recompensa
        if sucesso:
            sucessos_lote += 1


        if i % INTERVALO_RELATORIO == 0:
            media_passos = soma_passos / INTERVALO_RELATORIO
            media_reward = soma_reward / INTERVALO_RELATORIO
            taxa_sucesso = (sucessos_lote / INTERVALO_RELATORIO) * 100


            intervalo_str = f"{i - INTERVALO_RELATORIO + 1}-{i}"
            print(
                f"| {intervalo_str:^18} | {media_passos:^15.1f} | {media_reward:^15.1f} | {taxa_sucesso:^9.0f}% | {agente.epsilon:^8.2f} |")


            soma_passos = 0
            soma_reward = 0
            sucessos_lote = 0

    tempo_total = time.time() - tempo_inicio
    print("-" * 85)
    print(f"Treino concluído em {tempo_total:.2f} segundos.")


    print("\nA gerar gráfico de aprendizagem...")
    plt.figure(figsize=(10, 6))
    plt.plot(historico_passos, alpha=0.3, color='gray', label='Passos (Episódio)')

    # Calcular média móvel para o gráfico ficar mais "suave" e legível
    media_movel_janela = 20
    if len(historico_passos) > media_movel_janela:
        medias = [sum(historico_passos[i:i + media_movel_janela]) / media_movel_janela
                  for i in range(len(historico_passos) - media_movel_janela)]
        plt.plot(range(media_movel_janela, len(historico_passos)), medias,
                 color='blue', linewidth=2, label=f'Média Móvel ({media_movel_janela})')

    plt.title(f'Curva de Aprendizagem - {nome_prob}')
    plt.xlabel('Episódio')
    plt.ylabel('Passos até ao Objetivo')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


    print(f"\n--- MODO DEMONSTRAÇÃO (GUI) ---")
    input("Pressione ENTER para abrir a visualização...")

    agente.set_modo_teste(True)
    amb_teste = ambiente_classe()
    gui = VisualizadorGUI()

    try:
        passos, _, _ = rodar_episodio(agente, amb_teste, gui=gui)
        print(f"Demonstração terminada em {passos} passos.")
        input("Pressione ENTER na consola para sair...")
    except Exception as e:
        print(f"Erro na GUI: {e}")
    finally:
        gui.fechar()


if __name__ == "__main__":
    main()