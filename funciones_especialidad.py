import tkinter as tk
from tkinter import messagebox

# Variable interna de este módulo para guardar la especialidad
platillo_especial = None 

def abrir_ventana_personal(root):
    """
    Ventana para que el personal configure la especialidad.
    Recibe 'root' para saber de quién es hijo la ventana (Toplevel).
    """
    ventana_pers = tk.Toplevel(root)
    ventana_pers.title("Menú Personal - Agregar Especialidad")
    ventana_pers.geometry("400x400")

    tk.Label(ventana_pers, text="Agregar especialidad", font=("Arial", 12, "bold")).pack(pady=10)

    # Entradas de texto
    tk.Label(ventana_pers, text="Nombre de especialidad").pack(anchor="w", padx=20)
    entry_nombre = tk.Entry(ventana_pers, width=40)
    entry_nombre.pack(padx=20, pady=5)

    tk.Label(ventana_pers, text="Ingredientes").pack(anchor="w", padx=20)
    entry_ingred = tk.Entry(ventana_pers, width=40)
    entry_ingred.pack(padx=20, pady=5)

    tk.Label(ventana_pers, text="Costo especialidad").pack(anchor="w", padx=20)
    entry_costo = tk.Entry(ventana_pers, width=40)
    entry_costo.pack(padx=20, pady=5)

    def guardar():
        nombre = entry_nombre.get()
        ingredientes = entry_ingred.get()
        costo = entry_costo.get()

        if not nombre or not ingredientes or not costo:
            messagebox.showwarning("Faltan datos", "Llena todos los campos.")
            return

        try:
            val_costo = float(costo)
            # Guardamos en la variable global de ESTE archivo
            global platillo_especial
            platillo_especial = {
                "nombre": nombre,
                "ingredientes": ingredientes,
                "costo": val_costo
            }
            messagebox.showinfo("Éxito", f"Especialidad '{nombre}' guardada.")
            ventana_pers.destroy()
        except ValueError:
            messagebox.showerror("Error", "El costo debe ser numérico.")

    tk.Button(ventana_pers, text="AGREGAR AL MENÚ", bg="#ddd", command=guardar).pack(pady=20)


def ver_detalle_especialidad(root, cola_pedidos_compartida):
    """
    Ventana para que el alumno vea la especialidad y pida.
    Recibe:
      - root: para crear la ventana.
      - cola_pedidos_compartida: La lista del main.py para agregar el pedido.
    """
    if not platillo_especial:
        messagebox.showinfo("Aviso", "El personal aún no ha agregado la especialidad del día.")
        return

    ventana_det = tk.Toplevel(root)
    ventana_det.title("Detalle Especialidad")
    ventana_det.geometry("400x500")

    tk.Label(ventana_det, text="Especialidad del Día", font=("Arial", 12, "bold")).pack(pady=10)

    # Frame simulando la tarjeta de información
    frame = tk.LabelFrame(ventana_det, text="Información", padx=10, pady=10)
    frame.pack(padx=20, fill="x")

    tk.Label(frame, text=f"Platillo: {platillo_especial['nombre']}", font=("Arial", 10, "bold")).pack(anchor="w")
    tk.Label(frame, text=f"Ingredientes: {platillo_especial['ingredientes']}").pack(anchor="w")
    tk.Label(frame, text=f"Costo: ${platillo_especial['costo']}", fg="blue").pack(anchor="w")

    # Área de Extras
    tk.Label(ventana_det, text="Extras / Comentarios:").pack(anchor="w", padx=20, pady=(15,0))
    txt_extras = tk.Text(ventana_det, height=4, width=40)
    txt_extras.pack(padx=20)

    # Nombre del alumno
    tk.Label(ventana_det, text="Tu Nombre:").pack(anchor="w", padx=20, pady=(10,0))
    entry_cliente = tk.Entry(ventana_det, width=40)
    entry_cliente.pack(padx=20)

    def enviar():
        cliente = entry_cliente.get()
        extras = txt_extras.get("1.0", tk.END).strip()

        if not cliente:
            messagebox.showwarning("Error", "Escribe tu nombre.")
            return

        item_desc = f"Especialidad: {platillo_especial['nombre']}"
        if extras:
            item_desc += f" ({extras})"

        nuevo_pedido = {
            "cliente": cliente,
            "items": [item_desc],
            "total": platillo_especial['costo']
        }

        # Agregamos a la lista que viene del archivo main
        cola_pedidos_compartida.append(nuevo_pedido)
        
        messagebox.showinfo("Pedido Enviado", f"Total a pagar: ${platillo_especial['costo']}")
        ventana_det.destroy()

    tk.Button(ventana_det, text="ENVIAR SOLICITUD", bg="#4CAF50", fg="white", command=enviar).pack(pady=20)