import tkinter as tk
from tkinter import ttk
import os
import csv
import pandas as pd
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PerfisTab(ttk.Frame):
    def __init__(self, notebook):
        super().__init__(notebook)
        self.parent = notebook
        self.sistemas = []

        perfis_label = ttk.Label(self, text="Aba de Perfis", justify='center', font=("calibri", 20))
        perfis_label.pack(padx=10, pady=10)

        self.tree_consulta = ttk.Treeview(self, columns=("Sistema", "Perfil", "Descrição"), show="headings")
        self.tree_consulta.heading("#1", text="Sistema")
        self.tree_consulta.heading("#2", text="Perfil")
        self.tree_consulta.heading("#3", text="Descrição")
        self.tree_consulta.column("#1", width=100)
        self.tree_consulta.column("#2", width=150)
        self.tree_consulta.column("#3", width=500)
        self.tree_consulta.pack(padx=10, pady=10)

        nome_perfil_label = tk.Label(self, text="Nome do Perfil (máx. 20 caracteres):")
        nome_perfil_label.pack(padx=10, pady=5)
        self.nome_perfil_entry = tk.Entry(self)
        self.nome_perfil_entry.pack(padx=10, pady=5)

        descricao_perfil_label = tk.Label(self, text="Descrição do Perfil (máx. 200 caracteres):")
        descricao_perfil_label.pack(padx=10, pady=5)
        self.descricao_perfil_entry = tk.Entry(self)
        self.descricao_perfil_entry.pack(padx=10, pady=5)

        sistema_label = tk.Label(self, text="Selecione o Sistema:")
        sistema_label.pack(padx=10, pady=5)
        self.sistema_combobox = ttk.Combobox(self, state="readonly")
        self.sistema_combobox.pack(padx=10, pady=5)

        adicionar_button = tk.Button(self, text="Adicionar Perfil", command=self.adicionar_perfil)
        adicionar_button.pack(padx=10, pady=10)

        cancelar_button = tk.Button(self, text="Excluir Perfil", command=self.cancelar_adicao)
        cancelar_button.pack(padx=10, pady=10)

        self.carregar_sistemas_csv()
        self.carregar_dados_csv()
        self.start_file_observer()

    def carregar_sistemas_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "sistema.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            self.sistemas = df["Nome"].tolist()
            self.sistema_combobox["values"] = self.sistemas

    def adicionar_perfil(self):
        nome_perfil = self.nome_perfil_entry.get().strip().upper()
        descricao_perfil = self.descricao_perfil_entry.get().strip()
        sistema_selecionado = self.sistema_combobox.get()

        if not nome_perfil or not descricao_perfil or not sistema_selecionado:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        if len(descricao_perfil) > 200:
            messagebox.showwarning("Aviso", "A descrição do perfil não pode ter mais de 200 caracteres.")
            return

        self.tree_consulta.insert("", "end", values=(sistema_selecionado, nome_perfil, descricao_perfil))
        self.salvar_em_csv()

        self.nome_perfil_entry.delete(0, tk.END)
        self.descricao_perfil_entry.delete(0, tk.END)

        self.tree_sistemas.delete(*self.tree_sistemas.get_children())
        self.tree_sistemas.insert("", "end", values=self.sistemas)

        self.sistema_combobox["values"] = self.sistemas

    def salvar_em_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "perfis.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(["Sistema", "Perfil", "Descrição"])
            for item in self.tree_consulta.get_children():
                values = self.tree_consulta.item(item, "values")
                escritor.writerow(values)

    def carregar_dados_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "perfis.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "r", newline="", encoding="utf-8") as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                header = next(leitor)
                self.tree_consulta["columns"] = header
                self.tree_consulta.heading("#1", text=header[0])
                self.tree_consulta.heading("#2", text=header[1])
                self.tree_consulta.heading("#3", text=header[2])

                for linha in leitor:
                    self.tree_consulta.insert("", "end", values=linha)

    def cancelar_adicao(self):
        selecionado = self.tree_consulta.selection()
        if selecionado:
            self.tree_consulta.delete(selecionado)
            self.salvar_em_csv()
            print("Perfil excluído")

    def start_file_observer(self):
        csv_path = os.path.join(os.path.dirname(__file__), "sistema.csv")
        if os.path.exists(csv_path):
            event_handler = SistemaFileHandler(self)
            self.observer = Observer()
            self.observer.schedule(event_handler, path=os.path.dirname(__file__), recursive=False)
            self.observer.start()

    def stop_file_observer(self):
        self.observer.stop()
        self.observer.join()

class SistemaFileHandler(FileSystemEventHandler):
    def __init__(self, parent):
        self.parent = parent

    def on_modified(self, event):
        if event.src_path.endswith("sistema.csv"):
            self.parent.carregar_sistemas_csv()
            self.parent.sistema_combobox["values"] = self.parent.sistemas

if __name__ == "__main__":
    root = tk.Tk()
    app = PerfisTab(root)
    root.mainloop()
