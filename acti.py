import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
 
Ruta_del_Logo="impresora.ico"

# Base de datos en memoria (lista de diccionarios)
productos = []
contador_id = 1
 
# -------------------------------
# Funciones CRUD
# -------------------------------
def agregar_producto():
    global contador_id
    nombre = entry_nombre.get()
    categoria = entry_categoria.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    id_ingresado = entry_id.get()
 
    if not nombre or not categoria or not precio or not stock:
        messagebox.showwarning("Error", "Todos los campos son obligatorios")
        return
 
    try:
        precio = float(precio)
        stock = int(stock)
    except ValueError:
        messagebox.showwarning("Error", "Precio debe ser numero y Stock entero")
        return
 
    # Usar ID ingresado o autogenerar
    if id_ingresado.strip():
        try:
            id_producto = int(id_ingresado)
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un numero entero")
            return
    else:
        id_producto = contador_id
        contador_id += 1
 
    producto = {
        "id": id_producto,
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "stock": stock  
    }
    productos.append(producto)
    actualizar_tabla()
    limpiar_campos()
 
def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)
    for p in productos:
        tabla.insert("", "end", values=(p["id"], p["nombre"], p["categoria"], p["precio"], p["stock"]))
 
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)
    entry_id.delete(0, tk.END)
 
def seleccionar_producto(event):
    seleccionado = tabla.focus()
    if not seleccionado:
        return
    valores = tabla.item(seleccionado, "values")
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_stock.delete(0, tk.END)
 
    entry_id.insert(0, valores[0])
    entry_nombre.insert(0, valores[1])
    entry_categoria.insert(0, valores[2])
    entry_precio.insert(0, valores[3])
    entry_stock.insert(0, valores[4])
 
def editar_producto():
    seleccionado = tabla.focus()
    if not seleccionado:
        messagebox.showwarning("Error", "Selecciona un producto para editar")
        return
 
    try:
        precio = float(entry_precio.get())
        stock = int(entry_stock.get())
    except ValueError:
        messagebox.showwarning("Error", "Precio debe ser numero y Stock entero")
        return
 
    valores = tabla.item(seleccionado, "values")
    for p in productos:
        if p["id"] == int(valores[0]):
            p["id"] = int(entry_id.get())
            p["nombre"] = entry_nombre.get()
            p["categoria"] = entry_categoria.get()
            p["precio"] = precio
            p["stock"] = stock
            break
    actualizar_tabla()
    limpiar_campos()
 
def eliminar_producto():
    seleccionado = tabla.focus()
    if not seleccionado:
        messagebox.showwarning("Error", "Selecciona un producto para eliminar")
        return
    valores = tabla.item(seleccionado, "values")
    for p in productos:
        if p["id"] == int(valores[0]):
            productos.remove(p)
            break
    actualizar_tabla()
    limpiar_campos()
 
# -------------------------------
# Funcion de impresion
# -------------------------------
def imprimir_ticket():
    seleccionado = tabla.focus()
    if not seleccionado:
        messagebox.showwarning("Error", "Selecciona un producto para imprimir")
        return
 
    valores = tabla.item(seleccionado, "values")
    producto_id, nombre, categoria, precio, stock = valores
    stock = int(stock)
 
    if stock <= 0:
        messagebox.showwarning("Stock agotado", "No hay unidades disponibles")
        return
 
    # Actualizar stock en la base de datos
    for p in productos:
        if p["id"] == int(producto_id):
            p["stock"] -= 1
            stock = p["stock"]
            break
    actualizar_tabla()
 
    contenido = []
    contenido.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    contenido.append("== TIENDA ==\n")
    contenido.append(f"ID: {producto_id}\n")
    contenido.append(f"Producto: {nombre}\n")
    contenido.append(f"Categoria: {categoria}\n")
    contenido.append(f"Precio: {precio}\n")
    contenido.append(f"Stock restante: {stock}\n")
    contenido.append("Gracias por su compra!\n")
    contenido.append("\n\n\n")  # Espacio para corte
 
    archivo = "ticket.txt"
    with open(archivo, "w", encoding="utf-8") as f:
        f.write("".join(contenido))
 
    try:
        os.startfile(archivo, "print")
        messagebox.showinfo("Exito", "Ticket enviado a la impresora")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo imprimir: {e}")

# -------------------------------
# Funciones para el menú
# -------------------------------
def salir():
    """
    Cierra la aplicación
    """
    ventana.quit()

def mostrarAyuda():
    """
    Muestra ventana de ayuda
    """
    messagebox.showinfo("Ayuda", 
        "CRUD de Productos - Tienda\nEste programa permite gestionar productos:\n"
        "- Agregar\n- Editar\n- Eliminar\n- Imprimir Ticket"
    )

def mostrarInfo():
    """
    Muestra información acerca del programa
    """
    
    info = "Creado por Victor Cordoba\nVerison 1.0\n29/09/2025"
    messagebox.showinfo("Acerca de nosotros", info)
 
# -------------------------------
# Interfaz Tkinter
# -------------------------------
ventana = tk.Tk()
ventana.title("Tienda - CRUD de Productos")
ventana.geometry("1250x500")
 
frame_form = tk.Frame(ventana)
frame_form.pack(pady=10)
 
tk.Label(frame_form, text="ID:").grid(row=0, column=0, padx=5, pady=5)
entry_id = tk.Entry(frame_form)
entry_id.grid(row=0, column=1)
 
tk.Label(frame_form, text="Nombre:").grid(row=0, column=2, padx=5, pady=5)
entry_nombre = tk.Entry(frame_form)
entry_nombre.grid(row=0, column=3)
 
tk.Label(frame_form, text="Categoria:").grid(row=1, column=0, padx=5, pady=5)
entry_categoria = tk.Entry(frame_form)
entry_categoria.grid(row=1, column=1)
 
tk.Label(frame_form, text="Precio:").grid(row=1, column=2, padx=5, pady=5)
entry_precio = tk.Entry(frame_form)
entry_precio.grid(row=1, column=3)
 
tk.Label(frame_form, text="Stock:").grid(row=2, column=0, padx=5, pady=5)
entry_stock = tk.Entry(frame_form)
entry_stock.grid(row=2, column=1)
 
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)
 
tk.Button(frame_botones, text="Agregar", command=agregar_producto).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Editar", command=editar_producto).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Eliminar", command=eliminar_producto).grid(row=0, column=2, padx=5)
tk.Button(frame_botones, text="Limpiar", command=limpiar_campos).grid(row=0, column=3, padx=5)
tk.Button(frame_botones, text="Imprimir Ticket", command=imprimir_ticket).grid(row=0, column=4, padx=5)
 
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=10)
 
columnas = ("ID", "Nombre", "Categoria", "Precio", "Stock")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, anchor="center")
 
tabla.pack()
tabla.bind("<<TreeviewSelect>>", seleccionar_producto)

try:
    ventana.iconbitmap(Ruta_del_Logo)
except tk.TclError:
    print(f"No se pudo cargar el icono desde la ruta: {Ruta_del_Logo}")

# -------------------------------
# Barra de menú estilo calculadora
# -------------------------------
menubar = tk.Menu(ventana)

# Menú Inicio
menu_inicio = tk.Menu(menubar, tearoff=0)
menu_inicio.add_command(label="Agregar", command=agregar_producto)
menu_inicio.add_command(label="Editar", command=editar_producto)
menu_inicio.add_command(label="Eliminar", command=eliminar_producto)
menu_inicio.add_command(label="Limpiar", command=limpiar_campos)
menu_inicio.add_command(label="Imprimir Ticket", command=imprimir_ticket)
menu_inicio.add_separator()
menu_inicio.add_command(label="Salir", command=salir)
menubar.add_cascade(label="Inicio", menu=menu_inicio)

# Menú Ayuda
menu_ayuda = tk.Menu(menubar, tearoff=0)
menu_ayuda.add_command(label="Ayuda", command=mostrarAyuda)
menu_ayuda.add_command(label="Acerca de nosotros", command=mostrarInfo)
menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

# Asignar el menú a la ventana
ventana.config(menu=menubar)
 
ventana.mainloop()