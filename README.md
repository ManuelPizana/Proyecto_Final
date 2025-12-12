#  Sistema de Gestión de Pedidos para Cafetería

Este proyecto es una aplicación de escritorio desarrollada en **Python** utilizando la librería gráfica **Tkinter**. Su objetivo es simular y gestionar el flujo de trabajo de una cafetería escolar, facilitando la interacción entre los clientes (alumnos) y el personal de cocina (vendedores).

El sistema implementa una arquitectura basada en colas para el manejo de pedidos y cuenta con persistencia de datos básica mediante la generación de tickets en archivos de texto.

##  Características Principales

### Módulo de Alumno (Cliente)
* **Menú Interactivo:** Selección de productos mediante una interfaz intuitiva con casillas de verificación (Checkboxes).
* **Especialidad del Día:** Integración modular que permite consultar y agregar un platillo especial configurado por el administrador.
* **Carrito de Compras:** Cálculo automático del total a pagar en tiempo real.
* **Confirmación de Pedido:** Ventana de resumen (Pop-up) que permite revisar, editar o confirmar el pedido antes de enviarlo a la cocina.

### Módulo de Vendedor (Cocina/Admin)
* **Cola de Pedidos en Tiempo Real:** Visualización de los pedidos entrantes en una lista de espera (FIFO - First In, First Out).
* **Gestión de Despacho:** Sistema para procesar pedidos terminados.
* **Generación de Tickets:** Al despachar un pedido, el sistema permite guardar un recibo ("ticket") en formato `.txt` en la ubicación que el usuario elija.
* **Administración del Menú:** Acceso a la configuración para modificar la "Especialidad del día" (precio y descripción).

##  Aspectos Técnicos Destacados
* **Interfaz Gráfica (GUI):** Uso avanzado de widgets de Tkinter (`Toplevel`, `Listbox`, `Checkbutton`, `Entry`).
* **Manejo de Archivos (I/O):** Uso de `filedialog` para guardar registros de ventas externamente.
* **Estructuras de Datos:** Implementación de listas y diccionarios para manejar la cola de pedidos (`cola_pedidos`) y el inventario del menú.
* **Modularidad:** El código está estructurado para importar lógica externa (archivo `funciones_especialidad`), promoviendo buenas prácticas de programación.

##  Requisitos
* Python 3.x
* Librería estándar `tkinter` (incluida por defecto en Python)
* Archivo de imagen `logo_cafeteria.png` (opcional, para estética)
* Módulo `funciones_especialidadV03.py` (lógica backend adicional)

## Capturas de Pantalla

| Módulo de Alumno (Cliente) | Módulo de Vendedor (Admin) |
|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/e578011d-672c-47b1-856c-399d76d39c23" width="400"> | <img src="https://github.com/user-attachments/assets/20320ecd-6ce0-41de-9006-8aabd3bf5ba9" width="400"> |
| **Menú y Selección** | **Lista de Pedidos** |
| <img src="https://github.com/user-attachments/assets/a21aa047-b428-464e-8cb0-382c2021d8e0" width="400"> | <img src="https://github.com/user-attachments/assets/361bf635-b9e5-4851-b8d0-f1f9af6feb4f" width="400"> |
| **Resumen de Pedido** | **Administración** |

---
Desarrollado como parte de un proyecto de sistemas de control administrativo.

**Créditos:** @ManuelPizana & @Di3g0-ctrl
