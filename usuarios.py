import tkinter as tk
from tkinter import ttk
import os
import csv
import pandas as pd
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class UsuariosTab(ttk.Frame):
    def __init__(self, notebook):
        super().__init__(notebook)
        self.parent = notebook
        self.cpf_set = set()  # Rastreia os CPFs
        self.sistemas = []  # Lista de sistemas
        self.perfis = []  # Lista de perfis

        usuarios_label = ttk.Label(self, text="Aba de Usuários", justify='center', font=("calibri", 20))
        usuarios_label.pack(padx=10, pady=10)

        # Crie uma Treeview para exibir os usuários
        self.tree_usuarios = ttk.Treeview(self, columns=("CPF", "Sistema", "Perfil"), show="headings")
        self.tree_usuarios.heading("#1", text="CPF")
        self.tree_usuarios.heading("#2", text="Sistema")
        self.tree_usuarios.heading("#3", text="Perfil")
        self.tree_usuarios.column("#1", width=5)
        self.tree_usuarios.column("#2", width=5)
        self.tree_usuarios.column("#3", width=5)
        self.tree_usuarios["height"] = 10

        self.tree_usuarios.pack(padx=10, pady=10)

        # Entrada de CPF do Usuário
        cpf_label = tk.Label(self, text="CPF do Usuário (apenas números):")
        cpf_label.pack(padx=10, pady=5)
        self.cpf_entry = tk.Entry(self)
        self.cpf_entry.pack(padx=10, pady=5)

        # Lista suspensa para selecionar o sistema
        sistema_label = tk.Label(self, text="Selecione o Sistema:")
        sistema_label.pack(padx=10, pady=5)
        self.sistema_combobox = ttk.Combobox(self, state="readonly")
        self.sistema_combobox.pack(padx=10, pady=5)

        # Lista suspensa para selecionar o perfil
        perfil_label = tk.Label(self, text="Selecione o Perfil:")
        perfil_label.pack(padx=10, pady=5)
        self.perfil_combobox = ttk.Combobox(self, state="readonly")
        self.perfil_combobox.pack(padx=10, pady=5)

        # Botão de adicionar usuário
        adicionar_button = tk.Button(self, text="Adicionar Usuário", command=self.adicionar_usuario)
        adicionar_button.pack(padx=10, pady=10)
        # Botão Cancelar Usuário
        cancelar_button = tk.Button(self, text="Excluir Usuário", command=self.cancelar_usuario)
        cancelar_button.pack(padx=10, pady=10)

        # Carregar os dados dos sistemas do CSV
        self.carregar_sistemas_csv()

        # Carregar os dados dos perfis do CSV
        self.carregar_perfis_csv()

        # Carregar os dados dos usuários do CSV
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
            self.sistema_combobox["values"] = nomes_sistemas
            self.sistemas = nomes_sistemas  

    def carregar_perfis_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "perfis.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            nomes_perfis = df["Perfil"].tolist()
            self.perfil_combobox["values"] = nomes_perfis
            self.perfis = nomes_perfis  

    def adicionar_usuario(self):
        cpf = self.cpf_entry.get().strip()
        sistema = self.sistema_combobox.get()
        perfil = self.perfil_combobox.get()

        if not cpf.isdigit() or len(cpf) != 11:
            messagebox.showwarning("Aviso", "CPF inválido. Deve conter apenas 11 dígitos numéricos.")
            return

        # Verifique se o CPF já está cadastrado
        if cpf in self.cpf_set:
            # Encontre o índice do item duplicado
            item_duplicado = None
            for item in self.tree_usuarios.get_children():
                values = self.tree_usuarios.item(item, "values")
                if values[0].replace(".", "").replace("-", "") == cpf:
                    item_duplicado = item
                    break

            # Obtenha as informações do sistema e do perfil do item duplicado
            sistema_duplicado = self.tree_usuarios.item(item_duplicado, "values")[1]
            perfil_duplicado = self.tree_usuarios.item(item_duplicado, "values")[2]

            mensagem = f"O usuário com CPF {cpf} já foi cadastrado.\n"
            mensagem += f"Sistema: {sistema_duplicado}\n"
            mensagem += f"Perfil: {perfil_duplicado}"
            messagebox.showwarning("Conflito", mensagem)
            return

        # Formate o CPF com a máscara de CPF
        formatted_cpf = self.formatar_cpf(cpf)

        # Adicione o usuário à Treeview
        self.tree_usuarios.insert("", "end", values=(formatted_cpf, sistema, perfil))

        # Adicione o CPF ao conjunto
        self.cpf_set.add(cpf)

        # Salve em CSV
        self.salvar_em_csv()

        # Limpar o campo de entrada após adicionar o usuário
        self.cpf_entry.delete(0, tk.END)
        self.sistema_combobox.set('')
        self.perfil_combobox.set('')

    def formatar_cpf(self, cpf):
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    def salvar_em_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "usuarios.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(["CPF", "Sistema", "Perfil"])
            for item in self.tree_usuarios.get_children():
                values = self.tree_usuarios.item(item, "values")
                escritor.writerow(values)

    def carregar_dados_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "usuarios.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "r", newline="", encoding="utf-8") as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                header = next(leitor)
                self.tree_usuarios["columns"] = header
                self.tree_usuarios.heading("#1", text=header[0])
                self.tree_usuarios.heading("#2", text=header[1])
                self.tree_usuarios.heading("#3", text=header[2])
                for linha in leitor:
                    cpf = linha[0].replace(".", "").replace("-", "")
                    self.cpf_set.add(cpf)
                    self.tree_usuarios.insert("", "end", values=linha)

    def cancelar_usuario(self):
        selected_item = self.tree_usuarios.selection()
        if selected_item:
            cpf = self.tree_usuarios.item(selected_item, "values")[0]
            # Remova o usuário selecionado da Treeview
            self.tree_usuarios.delete(selected_item)
            # Remova o CPF do conjunto
            cpf = cpf.replace(".", "").replace("-", "")
            self.cpf_set.remove(cpf)
            # Salve a Treeview atualizada no arquivo CSV
            self.salvar_em_csv()

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
    app = UsuariosTab(root)
    root.mainloop()
