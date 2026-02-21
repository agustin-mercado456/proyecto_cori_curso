import tkinter as tk
from tkinter import ttk, messagebox
from models.cliente import Cliente
from controllers.cliente_controller import ClienteController

class ClienteCrudView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.controller = ClienteController()
        self.id_seleccionado = None 
        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        frame_form = tk.LabelFrame(self, text=" Datos del Cliente ", padx=10, pady=10, bg="white")
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        etiquetas = ["Razón Social", "CUIT/CUIL", "Rubro", "Direccion", "Localidad", "Provincia"]
        self.entries = {}

        for texto in etiquetas:
            tk.Label(frame_form, text=texto, bg="white").pack(anchor="w", pady=(5, 0))
            entry = tk.Entry(frame_form)
            entry.pack(fill="x", pady=2)
            self.entries[texto] = entry

        btn_frame = tk.Frame(frame_form, bg="white")
        btn_frame.pack(fill="x", pady=20)

        tk.Button(btn_frame, text="GUARDAR NUEVO", bg="#27ae60", fg="white", 
                  command=self.ejecutar_guardar, relief="flat", cursor="hand2").pack(fill="x", pady=5)
        
        tk.Button(btn_frame, text="ACTUALIZAR SELECCIONADO", bg="#f39c12", fg="white", 
                  command=self.ejecutar_actualizar, relief="flat", cursor="hand2").pack(fill="x", pady=5)
        
        tk.Button(btn_frame, text="LIMPIAR FORMULARIO", command=self.limpiar_form).pack(fill="x", pady=5)

        frame_tabla = tk.LabelFrame(self, text=" Clientes Registrados ", padx=10, pady=10, bg="white")
        frame_tabla.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        columnas = ("id", "razon", "cuit", "rubro", "dir", "loc", "prov")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        titulos = ["ID", "Razón Social", "CUIT", "Rubro", "Dirección", "Localidad", "Provincia"]
        for col, tit in zip(columnas, titulos):
            self.tree.heading(col, text=tit)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_registro)

        tk.Button(frame_tabla, text="ELIMINAR SELECCIONADO", bg="#c0392b", fg="white", 
                  command=self.ejecutar_eliminar, relief="flat").pack(fill="x", pady=10)

    def cargar_tabla(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for c in self.controller.listar_clientes():
            self.tree.insert("", "end", values=(c.id_cliente, c.razon_social, c.cuit_cuil, 
                                               c.rubro, c.direccion, c.localidad, c.provincia))

    def seleccionar_registro(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            d = self.tree.item(seleccion)['values']
            self.id_seleccionado = d[0]
            campos_ui = ["Razón Social", "CUIT/CUIL", "Rubro", "Direccion", "Localidad", "Provincia"]
            for i, campo in enumerate(campos_ui, 1):
                self.entries[campo].delete(0, tk.END)
                self.entries[campo].insert(0, d[i])

    def ejecutar_guardar(self):
        nuevo = Cliente(
            razon_social=self.entries["Razón Social"].get(),
            cuit_cuil=self.entries["CUIT/CUIL"].get(),
            rubro=self.entries["Rubro"].get(),
            direccion=self.entries["Direccion"].get(),
            localidad=self.entries["Localidad"].get(),
            provincia=self.entries["Provincia"].get()
        )
        exito, msj = self.controller.guardar_cliente(nuevo)
        if exito: 
            messagebox.showinfo("Éxito", msj)
            self.limpiar_form(); self.cargar_tabla()
        else: messagebox.showwarning("Atención", msj)

    def ejecutar_actualizar(self):
        if not self.id_seleccionado: return
        editado = Cliente(
            id_cliente=self.id_seleccionado,
            razon_social=self.entries["Razón Social"].get(),
            cuit_cuil=self.entries["CUIT/CUIL"].get(),
            rubro=self.entries["Rubro"].get(),
            direccion=self.entries["Direccion"].get(),
            localidad=self.entries["Localidad"].get(),
            provincia=self.entries["Provincia"].get()
        )
        exito, msj = self.controller.actualizar_cliente(editado)
        if exito: self.cargar_tabla()
        else: messagebox.showerror("Error", msj)

    def ejecutar_eliminar(self):
        if not self.id_seleccionado: return
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            self.controller.eliminar_cliente(self.id_seleccionado)
            self.limpiar_form(); self.cargar_tabla()

    def limpiar_form(self):
        self.id_seleccionado = None
        for e in self.entries.values(): e.delete(0, tk.END)