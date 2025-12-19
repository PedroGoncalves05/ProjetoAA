import tkinter as tk
from data_types import Posicao  # Necessário para testar a luz em cada célula


class VisualizadorGUI:
    def __init__(self, largura_grelha=10, altura_grelha=10, tamanho_celula=50):
        self.largura = largura_grelha
        self.altura = altura_grelha
        self.tamanho = tamanho_celula
        self.root = tk.Tk()
        self.root.title("Simulador SMA - Visualização")

        self.canvas = tk.Canvas(self.root, width=self.largura * self.tamanho,
                                height=self.altura * self.tamanho, bg="white")
        self.canvas.pack()

    def desenhar_ambiente(self, ambiente, agente):
        self.canvas.delete("all")

        metodo_luz = getattr(ambiente, '_esta_iluminado', None)
        if not metodo_luz:
            metodo_luz = getattr(ambiente, '_tem_linha_de_visao', None)

        for y in range(self.altura):
            for x in range(self.largura):
                x1 = x * self.tamanho
                x2 = x1 + self.tamanho
                y1 = y * self.tamanho
                y2 = y1 + self.tamanho

                cor = "white"
                e_obstaculo = False

                if hasattr(ambiente, 'grelha') and ambiente.grelha[y][x] == 1:
                    e_obstaculo = True
                elif hasattr(ambiente, 'obstaculos'):
                    if any(p.x == x and p.y == y for p in ambiente.obstaculos):
                        e_obstaculo = True

                if e_obstaculo:
                    cor = "black"
                elif metodo_luz:
                    pos_teste = Posicao(x, y)
                    if metodo_luz(pos_teste):
                        cor = "#FFFACD"  # Amarelo Claro (Luz)
                    else:
                        cor = "#F0F0F0"  # Cinza Claro (Sombra)
                else:
                    cor = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="#D3D3D3")

        pos_obj = getattr(ambiente, 'posicao_farol', None) or getattr(ambiente, 'posicao_final', None)
        if pos_obj:
            cx = pos_obj.x * self.tamanho
            cy = pos_obj.y * self.tamanho
            self.canvas.create_oval(cx + 5, cy + 5, cx + self.tamanho - 5, cy + self.tamanho - 5,
                                    fill="#00FF00", outline="darkgreen", width=2)

        pos_agente = ambiente.posicoes_agentes.get(agente.nome)
        if pos_agente:
            ax = pos_agente.x * self.tamanho
            ay = pos_agente.y * self.tamanho
            self.canvas.create_oval(ax + 10, ay + 10, ax + self.tamanho - 10, ay + self.tamanho - 10,
                                    fill="#4169E1", outline="darkblue", width=2)
            self.canvas.create_text(ax + self.tamanho / 2, ay + self.tamanho / 2,
                                    text="A", fill="white", font=("Arial", 12, "bold"))

        self.root.update()

    def fechar(self):
        self.root.destroy()