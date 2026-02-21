import tkinter as tk
from tkinter import messagebox
from views.view_cliente_crud import ClienteCrudView
from views.view_servicio_crud import ServicioCrudView
from views.view_presupuesto import PresupuestoForm # ¡Nuevo archivo que crearemos!

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Presupuestos - HyS")
        self.geometry("1100x650") 
        self.config(bg="#f0f0f0")
        
        self.eval('tk::PlaceWindow . center')
        self.crear_interfaz()

    def crear_interfaz(self):
        # --- HEADER ---
        header = tk.Frame(self, bg="#2c3e50", height=100)
        header.pack(fill="x")
        
        lbl_titulo = tk.Label(header, text="Sistema de Gestión HyS", 
                             bg="#2c3e50", fg="white", font=("Segoe UI", 24, "bold"))
        lbl_titulo.place(relx=0.5, rely=0.3, anchor="center")
        
        lbl_subtitulo = tk.Label(header, text="Seleccione una operación para comenzar", 
                                bg="#2c3e50", fg="#bdc3c7", font=("Segoe UI", 12))
        lbl_subtitulo.place(relx=0.5, rely=0.7, anchor="center")

        # --- CONTENEDOR CENTRAL ---
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20, pady=40)

        # Configuración de la grilla: 3 columnas centrales
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1)

        # --- TARJETAS ---
        
        # 1. CLIENTES (Púrpura)
        card_clientes = self.crear_tarjeta(main_frame, "Gestión de\nClientes", 
                                           "Administrar base de datos\n(Altas, Bajas, Modificaciones)",
                                           "#8e44ad", self.abrir_crud_clientes)
        card_clientes.grid(row=0, column=0, padx=15, sticky="nsew")

        # 2. NUEVO: PRESUPUESTADOR ÚNICO (Azul)
        card_presupuesto = self.crear_tarjeta(main_frame, "Generar\nPresupuesto", 
                                              "Crear presupuesto dinámico\npara todos los servicios",
                                              "#2980b9", self.abrir_presupuesto)
        card_presupuesto.grid(row=0, column=1, padx=15, sticky="nsew")

        # 3. SERVICIOS / CONFIG (Naranja)
        card_servicio = self.crear_tarjeta(main_frame, "Configuración\nde Servicios", 
                                             "Administrar catálogo de\nservicios y tarifas base",
                                             "#e67e22", self.abrir_crud_servicios)
        card_servicio.grid(row=0, column=2, padx=15, sticky="nsew")

        # --- FOOTER ---
        lbl_footer = tk.Label(self, text="Nada es tan importante, NI TAN URGENTE, que no pueda ser hecho con seguridad!",
                             font=("Segoe UI", 10, "italic"), bg="#f0f0f0", fg="#7f8c8d")
        lbl_footer.pack(side="bottom", pady=15)

    def crear_tarjeta(self, parent, titulo, descripcion, color_borde, comando):
        frame = tk.Frame(parent, bg="white", bd=1, relief="raised")
        tk.Frame(frame, bg=color_borde, height=10).pack(fill="x")
        container = tk.Frame(frame, bg="white")
        container.pack(expand=True, fill="both", padx=10, pady=10)
        
        tk.Label(container, text=titulo, font=("Segoe UI", 14, "bold"), bg="white", fg="#333").pack(pady=(10, 5))
        tk.Label(container, text=descripcion, font=("Segoe UI", 9), bg="white", fg="#666", height=3).pack(pady=(0, 10))
        
        tk.Button(container, text="INGRESAR ➤", bg=color_borde, fg="white", 
                        font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
                        command=comando).pack(pady=10, ipadx=15, ipady=5)
        return frame

    # --- ACCIONES ---
    def abrir_crud_clientes(self):
        top = tk.Toplevel(self)
        top.title("Administración de Clientes")
        top.geometry("1000x600")
        app = ClienteCrudView(top)
        app.pack(fill="both", expand=True)

    def abrir_crud_servicios(self):
        top = tk.Toplevel(self)
        top.title("Gestión de Tarifas de Servicios")
        top.geometry("1000x600")
        app = ServicioCrudView(top)
        app.pack(fill="both", expand=True)

    def abrir_presupuesto(self):
        top = tk.Toplevel(self)
        app = PresupuestoForm(top) # Llama a la nueva vista unificada

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()