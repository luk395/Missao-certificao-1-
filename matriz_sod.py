import tkinter as tk
from tkinter import ttk
import csv
from tkinter import messagebox
import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MatrizSodTab(ttk.Frame):
    def __init__(self, notebook):
        super().__init__(notebook)
        self.parent = notebook

        sod_label = ttk.Label(self, text="Matriz SoD (Segregation of Duties)", justify='center', font=("calibri", 14))
        sod_label.pack(padx=10, pady=10)

        # Crie uma Treeview para exibir a Matriz SoD
        self.tree_sod = ttk.Treeview(self, columns=("Sistema1", "Perfil1", "Sistema2", "Perfil2"), show="headings")
        self.tree_sod.heading("#1", text="Sistema 1")
        self.tree_sod.heading("#2", text="Perfil 1")
        self.tree_sod.heading("#3", text="Sistema 2")
        self.tree_sod.heading("#4", text="Perfil 2")
        self.tree_sod.column("#1", width=200)
        self.tree_sod.column("#2", width=150)
        self.tree_sod.column("#3", width=300)
        self.tree_sod.column("#4", width=150)
        self.tree_sod.pack(padx=5, pady=0)

        # Conjunto para manter as combinações existentes
        self.combinacoes_existentes = set()

        # Lista suspensa para selecionar o Sistema 1
        sistema1_label = tk.Label(self, text="Selecione o Sistema 1:")
        sistema1_label.pack(padx=10, pady=5)
        self.sistema1_combobox = ttk.Combobox(self, state="readonly")
        self.sistema1_combobox.pack(padx=10, pady=5)

        # Lista suspensa para selecionar o Perfil 1
        perfil1_label = tk.Label(self, text="Selecione o Perfil 1:")
        perfil1_label.pack(padx=10, pady=5)
        self.perfil1_combobox = ttk.Combobox(self, state="readonly")
        self.perfil1_combobox.pack(padx=10, pady=5)

        # Lista suspensa para selecionar o Sistema 2
        sistema2_label = tk.Label(self, text="Selecione o Sistema 2:")
        sistema2_label.pack(padx=10, pady=5)
        self.sistema2_combobox = ttk.Combobox(self, state="readonly")
        self.sistema2_combobox.pack(padx=10, pady=5)

        # Lista suspensa para selecionar o Perfil 2
        perfil2_label = tk.Label(self, text="Selecione o Perfil 2:")
        perfil2_label.pack(padx=10, pady=5)
        self.perfil2_combobox = ttk.Combobox(self, state="readonly")
        self.perfil2_combobox.pack(padx=10, pady=5)

        # Botão de adicionar conflito
        adicionar_button = tk.Button(self, text="Adicionar SoD", command=self.adicionar_sod)
        adicionar_button.pack(padx=10, pady=10)

        # Botão para remover conflito
        remover_button = tk.Button(self, text="Excluir SoD", command=self.remover_sod)
        remover_button.pack(padx=10, pady=10)

        # Carregar os dados dos sistemas do CSV
        self.carregar_sistemas_csv()

        # Carregar os dados dos perfis do CSV
        self.carregar_perfis_csv()

        # Carregar os dados da Matriz SoD do CSV
        self.carregar_dados_csv()

        # Iniciar o observador de arquivos para monitorar alterações no "sistema.csv"
        self.start_sistema_file_observer()

        # Iniciar o observador de arquivos para monitorar alterações no "perfis.csv"
        self.start_perfis_file_observer()

    def carregar_sistemas_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "sistema.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            nomes_sistemas = df["Nome"].tolist()
            self.sistema1_combobox["values"] = nomes_sistemas
            self.sistema2_combobox["values"] = nomes_sistemas
            self.sistemas = nomes_sistemas 
    def carregar_perfis_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "perfis.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            nomes_perfis = df["Perfil"].tolist()
            self.perfil1_combobox["values"] = nomes_perfis
            self.perfil2_combobox["values"] = nomes_perfis
            self.perfis = nomes_perfis 

    def adicionar_sod(self):
        sistema1 = self.sistema1_combobox.get()
        perfil1 = self.perfil1_combobox.get()
        sistema2 = self.sistema2_combobox.get()
        perfil2 = self.perfil2_combobox.get()

        if not sistema1 or not perfil1 or not sistema2 or not perfil2:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        # Verifique se os sistemas e perfis existem
        if sistema1 not in self.sistema1_combobox["values"] or perfil1 not in self.perfil1_combobox["values"] or sistema2 not in self.sistema2_combobox["values"] or perfil2 not in self.perfil2_combobox["values"]:
            messagebox.showwarning("Aviso", "Por favor, selecione sistemas e perfis válidos.")
            return

        # Verifique se a combinação já existe
        combinacao = (sistema1, perfil1, sistema2, perfil2)
        if combinacao in self.combinacoes_existentes:
            messagebox.showwarning("Aviso", "Essa combinação já existe na matriz.")
            return

        # Adicione a combinação à Treeview
        self.tree_sod.insert("", "end", values=combinacao)

        # Adicione a combinação ao conjunto de combinações existentes
        self.combinacoes_existentes.add(combinacao)

        # Salve em CSV
        self.salvar_em_csv()

        # Limpar os campos de entrada após adicionar a combinação
        self.sistema1_combobox.set('')
        self.perfil1_combobox.set('')
        self.sistema2_combobox.set('')
        self.perfil2_combobox.set('')

    def remover_sod(self):
        selected_item = self.tree_sod.selection()
        if selected_item:
            combinacao = tuple(self.tree_sod.item(selected_item, "values"))
            self.tree_sod.delete(selected_item)

            # Remova a combinação do conjunto de combinações existentes
            self.combinacoes_existentes.remove(combinacao)

            # Salvar em CSV após remover a combinação
            self.salvar_em_csv()

    def salvar_em_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "matriz_sod.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(["Sistema1", "Perfil1", "Sistema2", "Perfil2"])
            for item in self.tree_sod.get_children():
                values = self.tree_sod.item(item, "values")
                escritor.writerow(values)

    def carregar_dados_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "matriz_sod.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "r", newline="", encoding="utf-8") as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                header = next(leitor)
                self.tree_sod["columns"] = header
                for i, col_name in enumerate(header, start=1):
                    col_width = 150  # Defina a largura da coluna desejada
                    self.tree_sod.column("#{}".format(i), width=col_width)
                    self.tree_sod.heading("#{}".format(i), text=col_name)
                for linha in leitor:
                    combinacao = tuple(linha)
                    self.combinacoes_existentes.add(combinacao)
                    self.tree_sod.insert("", "end", values=combinacao)

    def start_sistema_file_observer(self):
        csv_path = os.path.join(os.path.dirname(__file__), "sistema.csv")
        if os.path.exists(csv_path):
            event_handler = SistemaFileHandler(self)
            self.sistema_observer = Observer()
            self.sistema_observer.schedule(event_handler, path=os.path.dirname(__file__), recursive=False)
            self.sistema_observer.start()

    def start_perfis_file_observer(self):
        csv_path = os.path.join(os.path.dirname(__file__), "perfis.csv")
        if os.path.exists(csv_path):
            event_handler = PerfisFileHandler(self)
            self.perfis_observer = Observer()
            self.perfis_observer.schedule(event_handler, path=os.path.dirname(__file__), recursive=False)
            self.perfis_observer.start()

class SistemaFileHandler(FileSystemEventHandler):
    def __init__(self, parent):
        self.parent = parent

    def on_modified(self, event):
        if event.src_path.endswith("sistema.csv"):
            self.parent.carregar_sistemas_csv()

class PerfisFileHandler(FileSystemEventHandler):
    def __init__(self, parent):
        self.parent = parent

    def on_modified(self, event):
        if event.src_path.endswith("perfis.csv"):
            self.parent.carregar_perfis_csv()

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrizSodTab(root)
    root.mainloop()

