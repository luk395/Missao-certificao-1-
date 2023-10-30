import tkinter as tk
from tkinter import ttk

# Classe HomeTab
class HomeTab(ttk.Frame):
    def __init__(self, notebook):
        super().__init__(notebook)


        home_label = ttk.Label(self, text="Bem-vindo!", justify='center', font=("calibri", 20))
        home_label.pack(padx=10, pady=80)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeTab(root)
    root.mainloop()