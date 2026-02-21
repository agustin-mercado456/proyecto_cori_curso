import tkinter as tk
from tkinter import messagebox
from models.cliente import Cliente
from services.cliente_service import ClienteService

class ClienteForm:
    def __init__(self, root, tipo_servicio):
        self.root = root
        self.tipo_servicio = tipo_servicio 
        self.service = ClienteService()
        self.root.title(f"Servicio: {tipo_servicio.upper()}")
        self.root.geometry("1100x700")
        self.dibujar_pantalla()

    def dibujar_pantalla(self):
        tk.Label(self.root, text=f"Presupuestador {self.tipo_servicio.capitalize()}", 
                 bg="#4CAF50", fg="white", font=("Arial", 16, "bold"), pady=10).pack(fill="x")

        pw = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        pw.pack(fill="both", expand=True, padx=10, pady=10)

        # IZQUIERDA
        f_nuevo = tk.LabelFrame(pw, text=" Registro Nuevo ", fg="green")
        pw.add(f_nuevo)
        self.entries = {}
        campos = ["Razón Social", "CUIT/CUIL", "Direccion", "Localidad", "Provincia", "Rubro"]
        for c in campos:
            tk.Label(f_nuevo, text=c).pack(anchor="w", padx=20)
            e = tk.Entry(f_nuevo); e.pack(fill="x", padx=20, pady=2)
            self.entries[c] = e
        tk.Button(f_nuevo, text="REGISTRAR", bg="#ff9800", command=self.guardar_nuevo_cliente).pack(pady=10)

        # DERECHA
        f_busq = tk.LabelFrame(pw, text=" Cliente Existente ", fg="blue")
        pw.add(f_busq)
        self.ent_buscar = tk.Entry(f_busq); self.ent_buscar.pack(padx=20, pady=10)
        tk.Button(f_busq, text="BUSCAR CUIT", command=self.buscar_cliente).pack()
        
        self.f_serv = tk.Frame(f_busq, bg="#eee"); self.f_serv.pack(fill="both", expand=True, pady=20)
        tk.Label(self.f_serv, text="Servicios Disponibles").pack()
        # Aquí irían los botones según el tipo de servicio...

    def guardar_nuevo_cliente(self):
        d = {k: v.get() for k, v in self.entries.items()}
        cliente = Cliente(razon_social=d["Razón Social"], cuit_cuil=d["CUIT/CUIL"], 
                         direccion=d["Direccion"], localidad=d["Localidad"], 
                         provincia=d["Provincia"], rubro=d["Rubro"])
        res = self.service.registrar_cliente(cliente)
        if res: messagebox.showinfo("OK", "Cliente registrado.")

    def buscar_cliente(self):
        cuit = self.ent_buscar.get()
        c = self.service.buscar_por_cuit(cuit)
        if c: messagebox.showinfo("Éxito", f"Cliente: {c.razon_social}")
        else: messagebox.showwarning("Error", "No existe.")