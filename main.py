import tkinter as tk
from tkinter import ttk
from desenvolvedores import Desenvolvedores
from home import HomeTab
from sistemas import SistemasTab
from perfis import PerfisTab
from usuarios import UsuariosTab
from matriz_sod import MatrizSodTab
from tkinter import messagebox

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("450x320")
        self.root.resizable(False, False)

        # login e senha de usuários
        self.user_credentials = {
            "admin": "admin123",
            "host": "host123"
        }

        # Imagem de login
        self.img = tk.PhotoImage(file="Login.png")
        self.lb_img = ttk.Label(root, image=self.img)
        self.lb_img.grid(row=3, column=0, padx=10)

        # Título
        self.title = ttk.Label(root, text='ESTACIO \nMISSAO CERTIFICAÇÃO 1 \nDEV Full Stack 2023.3 \nGrupo 4', font=("calibri", 12), justify="center")
        self.title.grid(row=0, column=0, pady=20, padx=10)

        # Frame de login
        self.frame_login = ttk.Frame(root, width=100, height=400)
        self.frame_login.place(x=200, y=20)

        # Título de login
        self.lb_title = ttk.Label(self.frame_login, text='Faça o seu Login', font=("calibri", 14))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        # Entrada de usuário
        self.sistemas_label = ttk.Entry(self.frame_login, width=30)
        self.sistemas_label.grid(row=1, column=0, pady=10, padx=10)
        self.sistemas_label.insert(0, 'Seu Usuário..')

        # Entrada de senha
        self.psw_login_entry = ttk.Entry(self.frame_login, width=30, show="*")
        self.psw_login_entry.grid(row=2, column=0, pady=10, padx=10)
        self.psw_login_entry.insert(0, 'Password..')

        # Botão de desenvolvedores
        btn_desenvolvedores = ttk.Button(self.frame_login, text='Desenvolvedores', command=self.abrir_desenvolvedores)
        btn_desenvolvedores.grid(row=4, column=0, pady=10, padx=10)

        # Botão de login
        self.btn_login = ttk.Button(self.frame_login, text='Fazer Login', command=self.verificar_login)
        self.btn_login.grid(row=3, column=0, pady=10, padx=10)

    def abrir_desenvolvedores(self):
        janela_desenvolvedores = tk.Toplevel(self.root)
        janela_desenvolvedores.title("Desenvolvedores")
        janela_desenvolvedores.geometry("600x200")
        janela_desenvolvedores.resizable(False, False)

        conteudo_desenvolvedores = Desenvolvedores(janela_desenvolvedores)

        janela_desenvolvedores.mainloop()

    def verificar_login(self):
        usuario = self.sistemas_label.get()
        senha = self.psw_login_entry.get()

        if usuario in self.user_credentials and self.user_credentials[usuario] == senha:
            perfil = usuario

            if perfil == "admin":
                self.abrir_home_admin()
            elif perfil == "host":
                self.abrir_home_host()
        else:
            messagebox.showerror("Erro de Login", "Credenciais inválidas. Tente novamente.")

    def abrir_home_admin(self):
        home = tk.Toplevel(self.root)
        home.title("Home (Perfil de Admin)")
        home.geometry("750x650")
        home.resizable(False, False)

        # Notebook (conjunto de abas)
        notebook = ttk.Notebook(home)
        notebook.pack(fill="both", expand=True)

        # Criando as abas
        home_tab = HomeTab(notebook)
        sistemas_tab = SistemasTab(notebook)
        perfis_tab = PerfisTab(notebook)
        usuarios_tab = UsuariosTab(notebook)
        matriz_sod_tab = MatrizSodTab(notebook)
 

        # Adicionando as abas ao Notebook
        notebook.add(home_tab, text="Home")
        notebook.add(sistemas_tab, text="Sistemas")
        notebook.add(perfis_tab, text="Perfis")
        notebook.add(matriz_sod_tab, text="Matriz SoD")
        notebook.add(usuarios_tab, text="Usuários")
        notebook.pack()

    def abrir_home_host(self):
        home = tk.Toplevel(self.root)
        home.title("Home (Perfil de Host)")
        home.geometry("750x650")
        home.resizable(False, False)

        # Notebook (conjunto de abas)
        notebook = ttk.Notebook(home)
        notebook.pack(fill="both", expand=True)

        # Criando as abas
        home_tab = HomeTab(notebook)
        sistemas_tab = SistemasTab(notebook)
        perfis_tab = PerfisTab(notebook)

        # Adicionando as abas ao Notebook
        notebook.add(home_tab, text="Home")
        notebook.add(sistemas_tab, text="Sistemas")
        notebook.add(perfis_tab, text="Perfis")

        notebook.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
