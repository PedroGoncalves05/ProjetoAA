import tkinter as tk
import time


class VisualizadorGUI:
    def __init__(self, largura_grelha=10, altura_grelha=10, tamanho_celula=50):
        self.largura = largura_grelha
        self.altura = altura_grelha
        self.tamanho = tamanho_celula


        self.root = tk.Tk()
        self.root.title("Simulador SMA - Visualização")


        self.canvas = tk.Canvas(
            self.root,
            width=self.largura * self.tamanho,
            height=self.altura * self.tamanho,
            bg="white"
        )
        self.canvas.pack()

    def desenhar_ambiente(self, ambiente, agente):
        """Atualiza o desenho da grelha com base no estado atual"""
        self.canvas.delete("all")


        for y in range(self.altura):
            for x in range(self.largura):
                x1 = x * self.tamanho
                y1 = (self.altura - 1 - y) * self.tamanho  # Inverter Y para (0,0) ser em baixo
                x2 = x1 + self.tamanho
                y2 = y1 + self.tamanho

                cor = "white"

                if hasattr(ambiente, 'grelha') and ambiente.grelha[y][x] == 1:
                    cor = "black"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="gray")


        pos_obj = getattr(ambiente, 'posicao_farol', None) or getattr(ambiente, 'posicao_final', None)

        if pos_obj:
            cx = pos_obj.x * self.tamanho
            cy = (self.altura - 1 - pos_obj.y) * self.tamanho
            self.canvas.create_oval(cx + 5, cy + 5, cx + self.tamanho - 5, cy + self.tamanho - 5, fill="green",
                                    outline="green")


        pos_agente = ambiente.posicoes_agentes.get(agente.nome)
        if pos_agente:
            ax = pos_agente.x * self.tamanho
            ay = (self.altura - 1 - pos_agente.y) * self.tamanho

            self.canvas.create_oval(ax + 10, ay + 10, ax + self.tamanho - 10, ay + self.tamanho - 10, fill="blue",
                                    outline="blue")


            self.canvas.create_text(ax + self.tamanho / 2, ay + self.tamanho / 2, text="A", fill="white")

        self.root.update()

    def fechar(self):
        self.root.destroy()