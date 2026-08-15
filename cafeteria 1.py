import tkinter as tk
import sqlite3


class CatalogoDB:

    def __init__(self):
        self.conn = sqlite3.connect("catalogo.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT NOT NULL,
                stock INT NOT NULL,
                precio REAL NOT NULL
            )
        """)
        self.conn.commit()

    def agregar(self, producto, stock, precio):
        self.cursor.execute(
            "INSERT INTO productos (producto, stock, precio) VALUES (?, ?, ?)",
            (producto, stock, precio)
        )
        self.conn.commit()

    def mostrar(self):
        self.cursor.execute("SELECT * FROM productos")
        return self.cursor.fetchall()

    def eliminar(self, id_producto):
        self.cursor.execute(
            "DELETE FROM productos WHERE id = ?",
            (id_producto,)
        )
        self.conn.commit()

    def actualizar(self, id_producto, producto, stock, precio):
        self.cursor.execute(
            "UPDATE productos SET producto = ?, stock = ?, precio = ? WHERE id = ?",
            (producto, stock, precio, id_producto)
        )
        self.conn.commit()


class Productos(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Cafetería UTZIN")
        self.geometry("400x500")

        self.bd = CatalogoDB()
        self.id_seleccionado = None

        self.__crear_widgets()
        self.__cargar_lista()

    def __crear_widgets(self):

        tk.Label(self, text="Producto").pack(pady=5)
        self.entry_producto = tk.Entry(self, width=35)
        self.entry_producto.pack()

        tk.Label(self, text="Stock").pack(pady=5)
        self.entry_stock = tk.Entry(self, width=35)
        self.entry_stock.pack()

        tk.Label(self, text="Precio").pack(pady=5)
        self.entry_precio = tk.Entry(self, width=35)
        self.entry_precio.pack()

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        tk.Button(
            frame_botones,
            text="Guardar",
            command=self._guardar
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            frame_botones,
            text="Actualizar",
            command=self._actualizar
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            frame_botones,
            text="Eliminar",
            command=self._eliminar
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            self,
            text="Consultar productos",
            command=self.__cargar_lista
        ).pack(pady=5)

        self.listbox = tk.Listbox(self, width=50, height=12)
        self.listbox.pack(pady=10)

        self.listbox.bind(
            "<<ListboxSelect>>",
            self._seleccionar
        )

    def _guardar(self):

        producto = self.entry_producto.get()
        stock = self.entry_stock.get()
        precio = self.entry_precio.get()

        if not producto.strip():
            return

        precio = self.__validar_precio(precio)

        self.bd.agregar(producto, stock, precio)

        self.__limpiar_entradas()
        self.__cargar_lista()

    def _seleccionar(self, event=None):

        seleccion = self.listbox.curselection()

        if not seleccion:
            return

        item = self.listbox.get(seleccion[0])
        id_producto = item.split(" - ")[0]

        datos = self.bd.mostrar()

        for producto in datos:

            if str(producto[0]) == id_producto:

                self.id_seleccionado = producto[0]

                self.entry_producto.delete(0, "end")
                self.entry_producto.insert(0, producto[1])

                self.entry_stock.delete(0, "end")
                self.entry_stock.insert(0, producto[2])

                self.entry_precio.delete(0, "end")
                self.entry_precio.insert(0, producto[3])

                break

    def _actualizar(self):

        if self.id_seleccionado is None:
            return

        producto = self.entry_producto.get()
        stock = self.entry_stock.get()
        precio = self.entry_precio.get()

        if not producto.strip():
            return

        precio = self.__validar_precio(precio)

        self.bd.actualizar(
            self.id_seleccionado,
            producto,
            stock,
            precio
        )

        self.__limpiar_entradas()
        self.__cargar_lista()

    def _eliminar(self):

        seleccion = self.listbox.curselection()

        if not seleccion:
            return

        item = self.listbox.get(seleccion[0])
        id_producto = item.split(" - ")[0]

        self.bd.eliminar(id_producto)

        self.__limpiar_entradas()
        self.__cargar_lista()

    def __validar_precio(self, precio):

        try:
            return float(precio)
        except ValueError:
            return 0.0

    def __limpiar_entradas(self):

        self.entry_producto.delete(0, "end")
        self.entry_stock.delete(0, "end")
        self.entry_precio.delete(0, "end")

        self.id_seleccionado = None
        self.listbox.selection_clear(0, "end")

    def __cargar_lista(self):

        self.listbox.delete(0, "end")

        datos = self.bd.mostrar()

        for producto in datos:
            texto = f"{producto[0]} - {producto[1]} ({producto[2]}) ${producto[3]}"
            self.listbox.insert("end", texto)


if __name__ == "__main__":
    app = Productos()
    app.mainloop()