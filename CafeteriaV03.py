import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# ARCHIVO DE ESPECIALIDAD
import funciones_especialidadV03

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

def mostrar_resumen(root, datos_pedido):
    """
    Muestra el resumen del pedido antes de confirmar.
    datos_pedido es un diccionario: {'cliente': str, 'items': list, 'total': int}
    """
    ventana_resumen = tk.Toplevel(root)
    ventana_resumen.title("Resumen de Pedido")
    ventana_resumen.geometry("400x500")

    tk.Label(ventana_resumen, text="Tu Pedido", font=("Arial", 14, "bold")).pack(pady=10)

    # Cuadro de lista para ver los items
    lista = tk.Listbox(ventana_resumen, width=40, height=10, font=("Arial", 11))
    lista.pack(padx=20, pady=5)

    for item in datos_pedido['items']:
        lista.insert(tk.END, f"- {item.capitalize()}")

    # Total
    tk.Label(ventana_resumen, text=f"Total a Pagar: ${datos_pedido['total']}", 
             font=("Arial", 12, "bold"), fg="blue").pack(pady=10)

    tk.Label(ventana_resumen, text=f"Cliente: {datos_pedido['cliente']}").pack()

    # --- LÓGICA DE BOTONES ---

    def confirmar_pedido():
        # Aquí es donde FINALMENTE se guarda en la cola global
        cola_pedidos.append(datos_pedido)
        messagebox.showinfo("Confirmado", "¡Tu pedido ha sido enviado a cocina!")
        ventana_resumen.destroy()

    def editar_pedido():
        # Cerramos el resumen y volvemos a abrir el menú, pasando los datos actuales
        ventana_resumen.destroy()
        abrir_ventana_alumno(root, pedido_existente=datos_pedido)

    # Botonera
    frame_botones = tk.Frame(ventana_resumen)
    frame_botones.pack(pady=20)

    btn_editar = tk.Button(frame_botones, text="Editar Pedido", width=15, command=editar_pedido)
    btn_editar.pack(side=tk.LEFT, padx=10)

    btn_confirmar = tk.Button(frame_botones, text="CONFIRMAR", width=15, bg="#4CAF50", fg="white", 
                              command=confirmar_pedido)
    btn_confirmar.pack(side=tk.LEFT, padx=10)


def abrir_ventana_alumno(root, pedido_existente=None):
    """
    Abre la ventana del menú.
    """
    ventana_alumno = tk.Toplevel(root)
    ventana_alumno.title("Menú Alumno")
    ventana_alumno.geometry("800x800")

    titulo = "Selecciona tus productos:"
    if pedido_existente:
        titulo = "Modificando pedido..."
    
    tk.Label(ventana_alumno, text=titulo, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    # Variables para guardar la especialidad
    especialidad_agregada = tk.BooleanVar(value=False)
    precio_especialidad = tk.IntVar(value=0)
    lbl_especialidad = tk.Label(ventana_alumno, text="(No agregada)", fg="gray", font=("Arial", 9))
    
    def ver_especialidad():
        """Abre la ventana de especialidad del día."""
        resultado = funciones_especialidadV03.ver_detalle_especialidad_con_retorno(root, cola_pedidos)
        if resultado:  # Si el usuario confirmó agregar
            especialidad_agregada.set(True)
            precio_especialidad.set(resultado["precio"])  # Guarda el precio
            lbl_especialidad.config(
                text=f"✓ {resultado['nombre']} (${resultado['precio']})", 
                fg="green", 
                font=("Arial", 9, "bold")
            )

    btn_esp = tk.Button(ventana_alumno, text=" Ver Especialidad del Día ", bg="#FFC107",
                        command=ver_especialidad, font=("Arial", 10, "bold"))
    btn_esp.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew", padx=20)

    lbl_especialidad.grid(row=2, column=0, columnspan=2, pady=5)

    vars_productos = {}
    fila_actual = 3

    items_previos = pedido_existente['items'] if pedido_existente else []

    for producto, precio in menu.items():
        var = tk.IntVar()
        
        if producto in items_previos:
            var.set(1)

        c = tk.Checkbutton(ventana_alumno, text=producto.capitalize(), variable=var, font=("Arial", 10))
        c.grid(row=fila_actual, column=0, sticky="w", padx=20)
        
        lbl_precio = tk.Label(ventana_alumno, text=f"${precio}", font=("Arial", 10))
        lbl_precio.grid(row=fila_actual, column=1, sticky="e", padx=20)
        
        vars_productos[producto] = var
        fila_actual += 1

    tk.Label(ventana_alumno, text="Tu Nombre:", font=("Arial", 10)).grid(row=fila_actual, column=0, columnspan=2, pady=(20, 5))
    fila_actual += 1
    
    entry_nombre = tk.Entry(ventana_alumno, font=("Arial", 10))
    entry_nombre.grid(row=fila_actual, column=0, columnspan=2, sticky="ew", padx=20)
    
    if pedido_existente:
        entry_nombre.insert(0, pedido_existente['cliente'])

    fila_actual += 1

    def ir_a_resumen():
        carrito = []
        total = 0
        cliente = entry_nombre.get()

        if not cliente:
            messagebox.showwarning("Error", "Por favor escribe tu nombre.")
            return

        # Agregar productos del menú estándar
        for producto, var in vars_productos.items():
            if var.get() == 1:
                carrito.append(producto)
                total += menu[producto]

        # Agregar especialidad si fue seleccionada
        if especialidad_agregada.get():
            carrito.append(funciones_especialidadV03.especialidad_del_dia["nombre"])
            total += precio_especialidad.get()  # Suma el precio guardado

        if carrito:
            datos_nuevos = {"cliente": cliente, "items": carrito, "total": total}
            ventana_alumno.destroy()
            mostrar_resumen(root, datos_nuevos)
        else:
            messagebox.showinfo("Vacío", "No seleccionaste nada del menú.")

    btn_siguiente = tk.Button(ventana_alumno, text="VER PEDIDO", bg="#2196F3", fg="white", 
                              width=20, font=("Arial", 10, "bold"), command=ir_a_resumen)
    btn_siguiente.grid(row=fila_actual, column=0, columnspan=2, pady=15, sticky="ew", padx=20)
    fila_actual += 1

    if pedido_existente:
        def cancelar_modificacion():
            ventana_alumno.destroy()
            mostrar_resumen(root, pedido_existente)

        btn_cancelar = tk.Button(ventana_alumno, text="Cancelar Modificación", fg="red", font=("Arial", 10),
                                command=cancelar_modificacion)
        btn_cancelar.grid(row=fila_actual, column=0, columnspan=2, pady=5, sticky="ew", padx=20)


def abrir_ventana_vendedor():
    ventana_vendedor = tk.Toplevel(root)
    ventana_vendedor.title("Cocina / Vendedor")
    ventana_vendedor.geometry("500x550")

    tk.Label(ventana_vendedor, text="Pedidos en Cola:", font=("Arial", 12, "bold")).pack(pady=10)

    lista_pedidos_widget = tk.Listbox(ventana_vendedor, width=70, height=15)
    lista_pedidos_widget.pack(pady=10)

    def actualizar_lista():
        lista_pedidos_widget.delete(0, tk.END)
        for pedido in cola_pedidos:
            texto = f"{pedido['cliente']} - ${pedido['total']} -> {', '.join(pedido['items'])}"
            lista_pedidos_widget.insert(tk.END, texto)

    actualizar_lista()

    def despachar_pedido():
        if cola_pedidos:
            pedido = cola_pedidos.pop(0)
            
            # --- LÓGICA PARA GENERAR Y GUARDAR EL ARCHIVO ---
            
            # 1. Crear el contenido del archivo de texto
            contenido = f"--- PEDIDO DESPACHADO ---\n"
            contenido += f"Cliente: {pedido['cliente']}\n"
            contenido += f"Total: ${pedido['total']}\n"
            contenido += "Items:\n"
            for item in pedido['items']:
                contenido += f"- {item.capitalize()}\n"
            
            # 2. Usar filedialog.asksaveasfile para abrir el diálogo de guardado
            nombre_sugerido = f"Pedido_{pedido['cliente'].replace(' ', '_')}.txt"
            
            f = filedialog.asksaveasfile(
                mode='w', 
                defaultextension=".txt",
                initialfile=nombre_sugerido,
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            
            if f is not None:
                try:
                    f.write(contenido)
                    messagebox.showinfo("Guardado", f"El pedido de {pedido['cliente']} ha sido guardado.")
                except Exception as e:
                    messagebox.showerror("Error de Guardado", f"Ocurrió un error al guardar: {e}")
                finally:
                    f.close()
            
            messagebox.showinfo("Cobro", f"Cobrar ${pedido['total']} a {pedido['cliente']}")
            actualizar_lista()
        else:
            messagebox.showinfo("Info", "No hay pedidos pendientes.")

    frame_botones = tk.Frame(ventana_vendedor)
    frame_botones.pack(pady=10)

    btn_despachar = tk.Button(frame_botones, text="DESPACHAR / COBRAR", bg="#FF5722", fg="white", command=despachar_pedido)
    btn_despachar.pack(side=tk.LEFT, padx=5)
    
    btn_actualizar = tk.Button(frame_botones, text="Refrescar Lista", command=actualizar_lista)
    btn_actualizar.pack(side=tk.LEFT, padx=5)

    # Separador
    tk.Frame(ventana_vendedor, height=2, bd=1, relief="sunken").pack(fill="x", padx=20, pady=15)
    
    tk.Label(ventana_vendedor, text="Administración del Menú:", font=("Arial", 10)).pack()
    
    btn_personal = tk.Button(ventana_vendedor, text="➕ Configurar Especialidad del Día", bg="#ddd", 
                             command=lambda: funciones_especialidadV03.abrir_ventana_personal(root))
    btn_personal.pack(pady=10)


# --- VENTANA PRINCIPAL (MAIN) ---

root = tk.Tk()
root.title("Sistema Cafetería vFinal")
root.geometry("800x700") 

try:
    imagen_original = tk.PhotoImage(file="logo_cafeteria.png")
    lbl_imagen = tk.Label(root, image=imagen_original)
    lbl_imagen.pack(pady=10)
except Exception:
    lbl_sin_imagen = tk.Label(root, text="logo_cafeteria.png (No encontrada)", fg="gray")
    lbl_sin_imagen.pack(pady=10)

lbl_titulo = tk.Label(root, text="Bienvenido a la Cafetería", font=("Helvetica", 14, "bold"))
lbl_titulo.pack(pady=10)

# Botones Principales
btn_alumno = tk.Button(root, text="Soy Alumno (Hacer Pedido)", width=30, height=2, command=lambda: abrir_ventana_alumno(root))
btn_alumno.pack(pady=10)

btn_vendedor = tk.Button(root, text="Soy Vendedor (Ver Pedidos)", width=30, height=2, command=abrir_ventana_vendedor)
btn_vendedor.pack(pady=10)

btn_salir = tk.Button(root, text="Salir", width=10, command=root.quit)
btn_salir.pack(pady=50)

root.mainloop()
