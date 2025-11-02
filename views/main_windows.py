# views/main_window.py

import tkinter as tk

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Mi Aplicación de Escritorio")
        self.master.geometry("800x600")  # tamaño por defecto, luego podemos leer config.py
        self.create_widgets()

    def create_widgets(self):
        # Label de bienvenida
        self.label = tk.Label(self.master, text="¡Bienvenido a la App!", font=("Arial", 20))
        self.label.pack(pady=50)

        # Botón de cerrar
        self.close_button = tk.Button(self.master, text="Cerrar", command=self.master.destroy)
        self.close_button.pack(pady=20)
