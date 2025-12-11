import tkinter as tk
from tkinter import messagebox, simpledialog


# Aquí guardamos la especialidad del día
especialidad_del_dia = {
    "nombre": "Pancakes Especiales",
    "precio": 35,
    "descripcion": "Pancakes con chocolate y fresas"
}


def ver_detalle_especialidad_con_retorno(root, cola_pedidos):
    """
    Abre una ventana para seleccionar la especialidad.
    Retorna un diccionario con nombre y precio, o None si cancela.
    """
    ventana_esp = tk.Toplevel(root)
    ventana_esp.title("Especialidad del Día")
    ventana_esp.geometry("400x300")
    ventana_esp.grab_set()  # Hace que sea modal
    
    tk.Label(ventana_esp, text="ESPECIALIDAD DEL DÍA", font=("Arial", 14, "bold"), fg="#FFC107").pack(pady=10)
    
    tk.Label(ventana_esp, text=especialidad_del_dia["nombre"], font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(ventana_esp, text=especialidad_del_dia["descripcion"], font=("Arial", 10), fg="gray").pack(pady=5)
    tk.Label(ventana_esp, text=f"Precio: ${especialidad_del_dia['precio']}", font=("Arial", 11, "bold"), fg="green").pack(pady=10)
    
    resultado = [None]  # Usamos lista para poder modificarla en la función anidada
    
    def confirmar():
        # RETORNA EL DICCIONARIO COMPLETO (nombre + precio)
        resultado[0] = {
            "nombre": especialidad_del_dia["nombre"],
            "precio": especialidad_del_dia["precio"]
        }
        ventana_esp.destroy()
    
    def cancelar():
        resultado[0] = None
        ventana_esp.destroy()
    
    frame_botones = tk.Frame(ventana_esp)
    frame_botones.pack(pady=20)
    
    tk.Button(frame_botones, text="Agregar a Pedido", bg="#4CAF50", fg="white", width=15, command=confirmar).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botones, text="Cancelar", width=15, command=cancelar).pack(side=tk.LEFT, padx=5)
    
    ventana_esp.wait_window()
    
    return resultado[0]



def ver_detalle_especialidad(root, cola_pedidos):
    """
    Función original (por compatibilidad).
    """
    return ver_detalle_especialidad_con_retorno(root, cola_pedidos)



def abrir_ventana_personal(root):
    """
    Permite configurar la especialidad del día.
    """
    ventana_config = tk.Toplevel(root)
    ventana_config.title("Configurar Especialidad del Día")
    ventana_config.geometry("400x350")
    
    tk.Label(ventana_config, text="Configurar Especialidad del Día", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(ventana_config, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_config, width=40)
    entry_nombre.pack(pady=5)
    entry_nombre.insert(0, especialidad_del_dia["nombre"])
    
    tk.Label(ventana_config, text="Descripción:").pack()
    entry_desc = tk.Entry(ventana_config, width=40)
    entry_desc.pack(pady=5)
    entry_desc.insert(0, especialidad_del_dia["descripcion"])
    
    tk.Label(ventana_config, text="Precio:").pack()
    entry_precio = tk.Entry(ventana_config, width=40)
    entry_precio.pack(pady=5)
    entry_precio.insert(0, str(especialidad_del_dia["precio"]))
    
    def guardar():
        global especialidad_del_dia
        try:
            especialidad_del_dia = {
                "nombre": entry_nombre.get(),
                "descripcion": entry_desc.get(),
                "precio": int(entry_precio.get())
            }
            messagebox.showinfo("Guardado", "Especialidad actualizada correctamente.")
            ventana_config.destroy()
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número.")
    
    tk.Button(ventana_config, text="Guardar Cambios", bg="#2196F3", fg="white", command=guardar).pack(pady=20)
