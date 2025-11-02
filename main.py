# main.py

import tkinter as tk
from views.main_windows import MainWindow

def main():
    # Crear la ventana raíz
    root = tk.Tk()

    # Inicializar la ventana principal (MainWindow)
    app = MainWindow(root)

    # Ejecutar loop de Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()
