import tkinter as tk
from tkinter import messagebox
import sqlite3


# Clase encargada de la base de datos
class CatalogoDB:

    def __init__(self):
        try:
            # Conectar con la base de datos
            self.conn = sqlite3.connect("catalogo.db")
            self.cursor = self.conn.cursor()

            # Crear la tabla si no existe
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto TEXT NOT NULL,
                    stock INTEGER NOT NULL,
                    precio REAL NOT NULL
                )
            """)

            self.conn.commit()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error de base de datos: {e}")

    # Agregar producto
    def agregar(self, producto, stock, precio):
        try:
            self.cursor.execute(
                "INSERT INTO productos (producto, stock, precio) VALUES (?, ?, ?)",
                (producto, stock, precio)
            )
            self.conn.commit()
            return True

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")
            return False

    # Mostrar productos
    def mostrar(self):
        try:
            self.cursor.execute("SELECT * FROM productos")
            return self.cursor.fetchall()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudieron mostrar los productos: {e}")
            return []

    # Actualizar producto
    def actualizar(self, id, producto, stock, precio):
        try:
            self.cursor.execute(
                "UPDATE productos SET producto=?, stock=?, precio=? WHERE id=?",
                (producto, stock, precio, id)
            )
            self.conn.commit()
            return True

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")
            return False

    # Eliminar producto
    def eliminar(self, id):
        try:
            self.cursor.execute(
                "DELETE FROM productos WHERE id=?",
                (id,)
            )
            self.conn.commit()
            return True

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
            return False


# Clase principal de la aplicación
class CafeteriaUtzinApp(tk.Tk):

    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("Cafeteria Utzin")
        self.geometry("400x500")

        # Crear conexión con la base de datos
        self.bd = CatalogoDB()

        # Guardará el ID del producto seleccionado
        self.id_seleccionado = None

        # Crear interfaz
        self.crear_interfaz()

        # Mostrar productos
        self.cargar_productos()


    def crear_interfaz(self):

        # Campo Producto
        tk.Label(self, text="Producto").pack(pady=5)

        self.producto = tk.Entry(self, width=35)
        self.producto.pack()


        # Campo Stock
        tk.Label(self, text="Stock").pack(pady=5)

        self.stock = tk.Entry(self, width=35)
        self.stock.pack()


        # Campo Precio
        tk.Label(self, text="Precio").pack(pady=5)

        self.precio = tk.Entry(self, width=35)
        self.precio.pack()


        # Botones
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Button(
            frame,
            text="Guardar",
            command=self.guardar
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            frame,
            text="Actualizar",
            command=self.actualizar
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            frame,
            text="Eliminar",
            command=self.eliminar
        ).grid(row=0, column=2, padx=5)


        # Lista de productos
        self.lista = tk.Listbox(
            self,
            width=55,
            height=12
        )
        self.lista.pack(pady=10)

        # Detectar cuando se selecciona un producto
        self.lista.bind(
            "<<ListboxSelect>>",
            self.seleccionar
        )


    def guardar(self):

        # Obtener los datos escritos
        producto = self.producto.get().strip()
        stock = self.stock.get().strip()
        precio = self.precio.get().strip()

        # Verificar que el producto tenga nombre
        if producto == "":
            messagebox.showwarning(
                "Advertencia",
                "Escribe el nombre del producto."
            )
            return

        # Convertir stock y precio a números
        try:
            stock = int(stock)
            precio = float(precio)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Stock debe ser entero y precio debe ser numérico."
            )
            return

        # Validar valores
        if stock < 0:
            messagebox.showwarning(
                "Advertencia",
                "El stock no puede ser negativo."
            )
            return

        if precio <= 0:
            messagebox.showwarning(
                "Advertencia",
                "El precio debe ser mayor a cero."
            )
            return

        # Guardar en la base de datos
        if self.bd.agregar(producto, stock, precio):

            messagebox.showinfo(
                "Éxito",
                "Producto guardado correctamente."
            )

            self.limpiar()
            self.cargar_productos()


    def seleccionar(self, event):

        # Obtener la posición seleccionada
        seleccion = self.lista.curselection()

        if not seleccion:
            return

        # Obtener el texto seleccionado
        texto = self.lista.get(seleccion[0])

        # Obtener el ID
        id_producto = texto.split(" - ")[0]

        # Buscar el producto en la base de datos
        for producto in self.bd.mostrar():

            if str(producto[0]) == id_producto:

                # Guardar el ID seleccionado
                self.id_seleccionado = producto[0]

                # Mostrar los datos en los campos
                self.producto.delete(0, tk.END)
                self.producto.insert(0, producto[1])

                self.stock.delete(0, tk.END)
                self.stock.insert(0, producto[2])

                self.precio.delete(0, tk.END)
                self.precio.insert(0, producto[3])

                break


    def actualizar(self):

        # Verificar que haya un producto seleccionado
        if self.id_seleccionado is None:
            messagebox.showwarning(
                "Advertencia",
                "Selecciona un producto."
            )
            return

        producto = self.producto.get().strip()
        stock = self.stock.get().strip()
        precio = self.precio.get().strip()

        if producto == "":
            messagebox.showwarning(
                "Advertencia",
                "Escribe el nombre del producto."
            )
            return

        # Convertir los datos
        try:
            stock = int(stock)
            precio = float(precio)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Stock debe ser entero y precio debe ser numérico."
            )
            return

        # Actualizar el producto
        if self.bd.actualizar(
            self.id_seleccionado,
            producto,
            stock,
            precio
        ):

            messagebox.showinfo(
                "Éxito",
                "Producto actualizado correctamente."
            )

            self.limpiar()
            self.cargar_productos()


    def eliminar(self):

        # Verificar que haya un producto seleccionado
        if self.id_seleccionado is None:
            messagebox.showwarning(
                "Advertencia",
                "Selecciona un producto."
            )
            return

        # Pedir confirmación
        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Deseas eliminar este producto?"
        )

        if confirmar:

            if self.bd.eliminar(self.id_seleccionado):

                messagebox.showinfo(
                    "Éxito",
                    "Producto eliminado correctamente."
                )

                self.limpiar()
                self.cargar_productos()


    def limpiar(self):

        # Borrar los campos
        self.producto.delete(0, tk.END)
        self.stock.delete(0, tk.END)
        self.precio.delete(0, tk.END)

        # Quitar la selección
        self.id_seleccionado = None
        self.lista.selection_clear(0, tk.END)


    def cargar_productos(self):

        # Limpiar la lista
        self.lista.delete(0, tk.END)

        # Obtener productos
        productos = self.bd.mostrar()

        # Mostrar cada producto
        for p in productos:

            texto = (
                f"{p[0]} - {p[1]} | "
                f"Stock: {p[2]} | "
                f"${p[3]:.2f}"
            )

            self.lista.insert(tk.END, texto)


# Iniciar el programa
if __name__ == "__main__":

    app = CafeteriaUtzinApp()
    app.mainloop()