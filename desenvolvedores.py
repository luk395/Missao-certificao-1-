import tkinter as tk
from tkinter import ttk

class Desenvolvedores(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        desenvolvedores_frame = ttk.Frame(self)
        desenvolvedores_frame.grid(row=0, column=0, sticky="nsew")

        dados_desenvolvedores = [
            ("Nome", "Matrícula"),
            ("LUCA MIGLIACCIO", "202307065765"),
            ("RAFAEL SANTOS CARNEIRO", "202307152374"),
        ]

        totalRows = len(dados_desenvolvedores)
        totalColumns = len(dados_desenvolvedores[0])

        for r in range(totalRows):
            for c in range(totalColumns):
                celula = ttk.Entry(desenvolvedores_frame, width=50, justify="center")
                celula.grid(row=r + 1, column=c, padx=0, pady=0, sticky="ns")
                celula.insert(0, dados_desenvolvedores[r][c])

if __name__ == "__main__":
    root = tk.Tk()
    desenvolvedores = Desenvolvedores(root)
    root.geometry("600x200")
    root.title("Desenvolvedores Grupo 4 - Turma 23.3")
    root.resizable(False, False)
    root.mainloop()
