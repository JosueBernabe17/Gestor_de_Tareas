import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Tarea:
    def __init__(self, nombre, hora=None, completada=False):
        self.nombre = nombre
        self.hora = hora or datetime.now().strftime("%H:%M")
        self.completada = completada

class AplicacionTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure("TButton", padding=5, font=('Arial', 10))
        self.style.configure("TLabel", font=('Arial', 10))
        self.style.configure("TEntry", padding=5)
        
        # Lista de tareas
        self.tareas = []
        
        # Frame principal
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        self.titulo = ttk.Label(
            self.main_frame, 
            text="📝 Lista de Tareas", 
            font=('Arial', 16, 'bold')
        )
        self.titulo.pack(pady=10)
        
        # Frame para entrada de tarea
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=10)
        
        # Campo de entrada
        self.entrada_tarea = ttk.Entry(self.input_frame, width=40)
        self.entrada_tarea.pack(side=tk.LEFT, padx=5)
        self.entrada_tarea.bind("<Return>", lambda e: self.agregar_tarea())
        
        # Botón agregar
        self.boton_agregar = ttk.Button(
            self.input_frame, 
            text="➕ Agregar", 
            command=self.agregar_tarea
        )
        self.boton_agregar.pack(side=tk.LEFT, padx=5)
        
        # Frame para la lista de tareas
        self.lista_frame = ttk.Frame(self.main_frame)
        self.lista_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Canvas y Scrollbar
        self.canvas = tk.Canvas(self.lista_frame, bg="white")
        self.scrollbar = ttk.Scrollbar(self.lista_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Botones de acción
        self.botones_frame = ttk.Frame(self.main_frame)
        self.botones_frame.pack(pady=10)
        
        self.boton_eliminar = ttk.Button(
            self.botones_frame,
            text="🗑️ Eliminar seleccionada",
            command=self.eliminar_tarea
        )
        self.boton_eliminar.pack(side=tk.LEFT, padx=5)
        
        self.boton_limpiar = ttk.Button(
            self.botones_frame,
            text="🧹 Limpiar completadas",
            command=self.limpiar_completadas
        )
        self.boton_limpiar.pack(side=tk.LEFT, padx=5)
        
        # Centrar la ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def agregar_tarea(self):
        tarea_texto = self.entrada_tarea.get().strip()
        if tarea_texto:
            tarea = Tarea(tarea_texto)
            self.tareas.append(tarea)
            
            # Crear frame para la tarea
            tarea_frame = ttk.Frame(self.scrollable_frame)
            tarea_frame.pack(fill=tk.X, pady=2)
            
            # Checkbox
            var = tk.BooleanVar(value=False)
            checkbox = ttk.Checkbutton(
                tarea_frame,
                variable=var,
                command=lambda t=tarea, v=var: self.marcar_completada(t, v)
            )
            checkbox.pack(side=tk.LEFT, padx=5)
            
            # Label con la tarea
            label = ttk.Label(
                tarea_frame,
                text=f"🕒 {tarea.hora} - {tarea.nombre}",
                font=('Arial', 10)
            )
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Guardar referencia a los widgets
            tarea.widgets = (tarea_frame, checkbox, label, var)
            
            self.entrada_tarea.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingresa una tarea")
    
    def marcar_completada(self, tarea, var):
        tarea.completada = var.get()
        _, checkbox, label, _ = tarea.widgets
        
        if tarea.completada:
            label.configure(foreground="gray")
            label.configure(font=('Arial', 10, 'overstrike'))
        else:
            label.configure(foreground="black")
            label.configure(font=('Arial', 10))
    
    def eliminar_tarea(self):
        for tarea in self.tareas[:]:
            if tarea.completada:
                tarea.widgets[0].destroy()
                self.tareas.remove(tarea)
    
    def limpiar_completadas(self):
        tareas_completadas = [t for t in self.tareas if t.completada]
        if not tareas_completadas:
            messagebox.showinfo("Información", "No hay tareas completadas para limpiar")
            return
        
        for tarea in tareas_completadas:
            tarea.widgets[0].destroy()
            self.tareas.remove(tarea)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionTareas(root)
    root.mainloop()
