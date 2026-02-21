import tkinter as tk
from tkinter import ttk, messagebox
from models.tipo_servicio import TipoServicio
from controllers.servicio_controller import ServicioController

class ServicioCrudView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.controller = ServicioController()
        self.id_seleccionado = None 
        self.crear_interfaz()
        self.cargar_tabla()

    def crear_interfaz(self):
        # --- PANEL IZQUIERDO: FORMULARIO ---
        frame_form = tk.LabelFrame(self, text=" Configuración del Servicio ", padx=10, pady=10, bg="white")
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        # Campos específicos para Servicios
        self.etiquetas = ["Nombre del Servicio", "Descripción", "Tarifa Base ($)"]
        self.entries = {}

        for texto in self.etiquetas:
            tk.Label(frame_form, text=texto, bg="white").pack(anchor="w", pady=(5, 0))
            if texto == "Descripción":
                # La descripción suele ser más larga, pero usamos Entry para mantener la estética simple por ahora
                entry = tk.Entry(frame_form)
            else:
                entry = tk.Entry(frame_form)
            
            entry.pack(fill="x", pady=2)
            self.entries[texto] = entry

        # Checkbox para el estado Activo/Inactivo
        self.var_activo = tk.BooleanVar(value=True)
        self.chk_activo = tk.Checkbutton(frame_form, text="Servicio Activo", variable=self.var_activo, bg="white")
        self.chk_activo.pack(anchor="w", pady=10)

        btn_frame = tk.Frame(frame_form, bg="white")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="GUARDAR NUEVO", bg="#27ae60", fg="white", 
                  command=self.ejecutar_guardar, relief="flat", cursor="hand2").pack(fill="x", pady=5)
        
        tk.Button(btn_frame, text="ACTUALIZAR SELECCIONADO", bg="#f39c12", fg="white", 
                  command=self.ejecutar_actualizar, relief="flat", cursor="hand2").pack(fill="x", pady=5)
        
        tk.Button(btn_frame, text="LIMPIAR FORMULARIO", command=self.limpiar_form).pack(fill="x", pady=5)

        # --- PANEL DERECHO: TABLA ---
        frame_tabla = tk.LabelFrame(self, text=" Catálogo de Servicios Higiene y Seguridad ", padx=10, pady=10, bg="white")
        frame_tabla.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        columnas = ("id", "nombre", "descripcion", "tarifa", "estado")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        titulos = ["ID", "Nombre", "Descripción", "Tarifa Base", "Estado"]
        anchos = [40, 200, 250, 100, 80]
        
        for col, tit, anc in zip(columnas, titulos, anchos):
            self.tree.heading(col, text=tit)
            self.tree.column(col, width=anc)
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_registro)

        tk.Button(frame_tabla, text="DESACTIVAR SERVICIO (BAJA LÓGICA)", bg="#c0392b", fg="white", 
                  command=self.ejecutar_eliminar, relief="flat").pack(fill="x", pady=10)

    def cargar_tabla(self):
        # Limpiar tabla
        for item in self.tree.get_children(): self.tree.delete(item)
        
        # Cargar todos (activos e inactivos para gestión)
        servicios = self.controller.listar_servicios(solo_activos=False)
        for s in servicios:
            estado = "Activo" if s.activo else "Inactivo"
            self.tree.insert("", "end", values=(s.id_tipo_servicio, s.nombre, s.descripcion, 
                                               f"${s.tarifa_base:,.2f}", estado))

    def seleccionar_registro(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            d = self.tree.item(seleccion)['values']
            self.id_seleccionado = d[0]
            
            # El valor de la tarifa viene con "$" y "," por el formato, hay que limpiarlo
            tarifa_limpia = str(d[3]).replace("$", "").replace(",", "")
            
            self.entries["Nombre del Servicio"].delete(0, tk.END)
            self.entries["Nombre del Servicio"].insert(0, d[1])
            self.entries["Descripción"].delete(0, tk.END)
            self.entries["Descripción"].insert(0, d[2])
            self.entries["Tarifa Base ($)"].delete(0, tk.END)
            self.entries["Tarifa Base ($)"].insert(0, tarifa_limpia)
            
            self.var_activo.set(True if d[4] == "Activo" else False)

    def ejecutar_guardar(self):
        try:
            nuevo = TipoServicio(
                nombre=self.entries["Nombre del Servicio"].get(),
                descripcion=self.entries["Descripción"].get(),
                tarifa_base=float(self.entries["Tarifa Base ($)"].get() or 0)
            )
            exito, msj = self.controller.guardar_servicio(nuevo)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.limpiar_form(); self.cargar_tabla()
            else:
                messagebox.showwarning("Atención", msj)
        except ValueError:
            messagebox.showerror("Error", "La tarifa debe ser un número válido.")

    def ejecutar_actualizar(self):
        if not self.id_seleccionado: 
            return messagebox.showwarning("Atención", "Seleccione un servicio de la tabla.")
        
        try:
            editado = TipoServicio(
                id_tipo_servicio=self.id_seleccionado,
                nombre=self.entries["Nombre del Servicio"].get(),
                descripcion=self.entries["Descripción"].get(),
                tarifa_base=float(self.entries["Tarifa Base ($)"].get() or 0),
                activo=self.var_activo.get()
            )
            exito, msj = self.controller.modificar_servicio(editado)
            if exito:
                messagebox.showinfo("Éxito", msj)
                self.limpiar_form(); self.cargar_tabla()
            else:
                messagebox.showerror("Error", msj)
        except ValueError:
            messagebox.showerror("Error", "La tarifa debe ser un número válido.")

    def ejecutar_eliminar(self):
        if not self.id_seleccionado: return
        if messagebox.askyesno("Confirmar", "¿Desea desactivar este servicio del catálogo?\nNo se borrará el historial."):
            exito, msj = self.controller.eliminar_servicio(self.id_seleccionado)
            if exito:
                self.limpiar_form(); self.cargar_tabla()
            else:
                messagebox.showerror("Error", msj)

    def limpiar_form(self):
        self.id_seleccionado = None
        for e in self.entries.values(): e.delete(0, tk.END)
        self.var_activo.set(True)