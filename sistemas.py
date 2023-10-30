import tkinter as tk
from tkinter import ttk
import os
import csv
from tkinter import messagebox

class SistemasTab(ttk.Frame):
    def __init__(self, notebook):
        super().__init__(notebook)
        self.parent = notebook

        sistemas_label = ttk.Label(self, text="Sistemas Cadastrados", justify='center', font=("calibri", 14))
        sistemas_label.pack(padx=10, pady=10)

        self.tree_consulta = ttk.Treeview(self, columns=("Codigo", "Nome"), show="headings")
        self.tree_consulta.heading("#1", text="Código")
        self.tree_consulta.heading("#2", text="Nome do Sistema")
        self.tree_consulta.column("#1", width=80)
        self.tree_consulta.column("#2", width=150)
        self.tree_consulta.pack(padx=10, pady=10)

        codigo_label = tk.Label(self, text="Código do Sistema:")
        codigo_label.pack(padx=10, pady=5)
        self.codigo_entry = tk.Entry(self)
        self.codigo_entry.pack(padx=10, pady=5)

        nome_label = tk.Label(self, text="Nome do Sistema:")
        nome_label.pack(padx=10, pady=5)
        self.nome_entry = tk.Entry(self)
        self.nome_entry.pack(padx=10, pady=5)

        # Botão de adicionar sistema
        adicionar_button = tk.Button(self, text="Adicionar Sistema", command=self.adicionar_sistema)
        adicionar_button.pack(padx=10, pady=10)

        # Botão para cancelar sistema selecionado
        cancelar_button = tk.Button(self, text="Cancelar Sistema", command=self.cancelar_sistema)
        cancelar_button.pack(padx=10, pady=10)

        # Carregar os dados do CSV na Treeview
        self.carregar_dados_csv()

    def adicionar_sistema(self):
        codigo = self.codigo_entry.get().strip().upper()
        nome = self.nome_entry.get().strip().upper()

        if not codigo or not nome:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        sistema_existente = None
        for item in self.tree_consulta.get_children():
            if self.tree_consulta.item(item, "values")[0] == codigo:
                sistema_existente = self.tree_consulta.item(item, "values")[0]
                break

        if sistema_existente:
            messagebox.showwarning("Aviso", f"O sistema {sistema_existente} já foi adicionado.")
        else:
            self.salvar_em_csv(codigo, nome)
            self.tree_consulta.insert("", tk.END, values=(codigo, nome))
            self.codigo_entry.delete(0, tk.END)
            self.nome_entry.delete(0, tk.END)

    def cancelar_sistema(self):
        selected_item = self.tree_consulta.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione um sistema para cancelar.")
            return

        sistema_codigo = self.tree_consulta.item(selected_item, "values")[0]
        self.remover_sistema_do_csv(sistema_codigo)
        self.tree_consulta.delete(selected_item)

    def salvar_em_csv(self, codigo, nome):
        csv_path = os.path.join(os.path.dirname(__file__), "sistema.csv")
        with open(csv_path, "a", newline="", encoding="utf-8") as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow([codigo, nome])

    def carregar_dados_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "sistema.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "r", newline="", encoding="utf-8") as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                next(leitor, None)
                for linha in leitor:
                    self.tree_consulta.insert("", tk.END, values=(linha[0], linha[1]))

    def remover_sistema_do_csv(self, codigo):
        csv_path = os.path.join(os.path.dirname(__file__), "sistema.csv")
        temp_path = os.path.join(os.path.dirname(__file__), "temp.csv")

        with open(csv_path, "r", newline="", encoding="utf-8") as arquivo_csv, open(temp_path, "w", newline="", encoding="utf-8") as temp_csv:
            leitor = csv.reader(arquivo_csv)
            escritor = csv.writer(temp_csv)

            header = next(leitor)
            escritor.writerow(header)

            for linha in leitor:
                if linha[0] != codigo:
                    escritor.writerow(linha)

        os.remove(csv_path)
        os.rename(temp_path, csv_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemasTab(root)
    root.mainloop()
