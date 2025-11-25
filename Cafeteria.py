import tkinter as tk
from tkinter import messagebox 

# --- DATOS Y LÓGICA (BACKEND) ---
menu = {
    "cafe": 20,
    "sandwich": 30,
    "jugo": 20,
    "mollete": 20,
    "Torta": 55
}

cola_pedidos = []

# --- FUNCIONES DE LA INTERFAZ (FRONTEND) ---

def abrir_ventana_alumno():
    ventana_alumno = tk.Toplevel(root)
    ventana_alumno.title("Menú Alumno")
    ventana_alumno.geometry("800x700")

    # Título
    tk.Label(ventana_alumno, text="Selecciona tus productos:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    vars_productos = {}
    fila_actual = 1

    # Generar el menú usando .grid() para que quede alineado
    for producto, precio in menu.items():
        var = tk.IntVar()
        
        # Nombre del producto (Izquierda)
        c = tk.Checkbutton(ventana_alumno, text=producto.capitalize(), variable=var)
        c.grid(row=fila_actual, column=0, sticky="w", padx=20)
        
        # Precio (Derecha)
        lbl_precio = tk.Label(ventana_alumno, text=f"${precio}")
        lbl_precio.grid(row=fila_actual, column=1, sticky="e", padx=20)
        
        vars_productos[producto] = var
        fila_actual += 1

    # Función interna para enviar
    def enviar_pedido():
        carrito = []
        total = 0
        cliente = entry_nombre.get()

        if not cliente:
            messagebox.showwarning("Error", "Por favor escribe tu nombre.")
            return

        for producto, var in vars_productos.items():
            if var.get() == 1:
                carrito.append(producto)
                total += menu[producto]

        if carrito:
            nuevo_pedido = {"cliente": cliente, "items": carrito, "total": total}
            cola_pedidos.append(nuevo_pedido)
            messagebox.showinfo("Éxito", f"Pedido enviado a cocina.\nTotal a pagar: ${total}")
            ventana_alumno.destroy()
        else:
            messagebox.showinfo("Vacío", "No seleccionaste nada.")

    # Campo Nombre y Botón
    tk.Label(ventana_alumno, text="Tu Nombre:").grid(row=fila_actual, column=0, columnspan=2, pady=(20, 5))
    fila_actual += 1
    
    entry_nombre = tk.Entry(ventana_alumno)
    entry_nombre.grid(row=fila_actual, column=0, columnspan=2)
    fila_actual += 1

    btn_enviar = tk.Button(ventana_alumno, text="ENVIAR PEDIDO", bg="#4CAF50", fg="white", command=enviar_pedido)
    btn_enviar.grid(row=fila_actual, column=0, columnspan=2, pady=20)


def abrir_ventana_vendedor():
    ventana_vendedor = tk.Toplevel(root)
    ventana_vendedor.title("Cocina / Vendedor")
    ventana_vendedor.geometry("400x400")

    tk.Label(ventana_vendedor, text="Pedidos en Cola:", font=("Arial", 12, "bold")).pack(pady=10)

    lista_pedidos_widget = tk.Listbox(ventana_vendedor, width=50, height=15)
    lista_pedidos_widget.pack(pady=10)

    def actualizar_lista():
        lista_pedidos_widget.delete(0, tk.END)
        for pedido in cola_pedidos:
            texto = f"{pedido['cliente']} - ${pedido['total']} ({', '.join(pedido['items'])})"
            lista_pedidos_widget.insert(tk.END, texto)

    actualizar_lista()

    def despachar_pedido():
        if cola_pedidos:
            pedido = cola_pedidos.pop(0)
            messagebox.showinfo("Cobro", f"Cobrar ${pedido['total']} a {pedido['cliente']}")
            actualizar_lista()
        else:
            messagebox.showinfo("Info", "No hay pedidos pendientes.")

    btn_despachar = tk.Button(ventana_vendedor, text="DESPACHAR / COBRAR", bg="#FF5722", fg="white", command=despachar_pedido)
    btn_despachar.pack(pady=10)
    
    btn_actualizar = tk.Button(ventana_vendedor, text="Refrescar Lista", command=actualizar_lista)
    btn_actualizar.pack()

# --- VENTANA PRINCIPAL (MAIN) ---

root = tk.Tk()
root.title("Sistema Cafetería vFinal")
root.geometry("800x700") 

# 1. INTENTO DE CARGAR LA IMAGEN
# El archivo debe llamarse 'logo_cafeteria.png' y estar junto a este script
try:
    # Cargamos la imagen
    imagen_original = tk.PhotoImage(file="logo_cafeteria.png")
    
    # Creamos un Label para mostrarla
    lbl_imagen = tk.Label(root, image=imagen_original)
    lbl_imagen.pack(pady=10)
    
except Exception:
    # Si falla (no existe la imagen), mostramos un texto simple en su lugar
    print("Nota: No se encontró 'logo_cafeteria.png', se usará texto.")
    lbl_sin_imagen = tk.Label(root, text="[AQUI IRÍA TU LOGO]", fg="gray")
    lbl_sin_imagen.pack(pady=10)

# Título y Botones
lbl_titulo = tk.Label(root, text="Bienvenido a la Cafetería", font=("Helvetica", 14, "bold"))
lbl_titulo.pack(pady=10)

btn_alumno = tk.Button(root, text="Soy Alumno (Hacer Pedido)", width=25, height=2, command=abrir_ventana_alumno)
btn_alumno.pack(pady=10)

btn_vendedor = tk.Button(root, text="Soy Vendedor (Ver Pedidos)", width=25, height=2, command=abrir_ventana_vendedor)
btn_vendedor.pack(pady=10)

btn_salir = tk.Button(root, text="Salir", width=10, command=root.quit)
btn_salir.pack(pady=20)

root.mainloop()