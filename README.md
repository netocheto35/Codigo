# ☕ Sistema de Inventario - Cafetería Utzin

Una aplicación de escritorio ligera e intuitiva diseñada para gestionar el catálogo de productos de una cafetería. Desarrollada en **Python**, utiliza **Tkinter** para la interfaz gráfica y **SQLite3** para el almacenamiento local de datos.

## 🚀 Características Principales (CRUD)

*   **Crear:** Agrega nuevos productos indicando su nombre, cantidad en stock y precio.
*   **Leer:** Visualiza en tiempo real el catálogo completo de productos disponibles.
*   **Actualizar:** Selecciona cualquier producto de la lista para modificar rápidamente su información.
*   **Eliminar:** Borra productos del inventario de forma segura gracias a una ventana emergente de confirmación.
*   **Validaciones:** El sistema protege la base de datos evitando el guardado de texto en campos numéricos, stocks negativos o precios en cero.

## 🛠️ Tecnologías y Requisitos

Este proyecto es completamente autónomo y utiliza exclusivamente herramientas de la biblioteca estándar de Python. **No requiere la instalación de librerías externas** mediante `pip`.

*   **Lenguaje:** Python 3.6 o superior.
*   **Interfaz Gráfica:** `tkinter` (Incluido por defecto en Python).
*   **Base de Datos:** `sqlite3` (Incluido por defecto en Python).

## ⚙️ Instalación y Uso

1. Asegúrate de tener [Python](https://www.python.org/downloads/) instalado en tu computadora.
2. Descarga el código fuente y guárdalo en un archivo, por ejemplo: `cafeteria.py`.
3. Abre una terminal o símbolo del sistema en la carpeta donde guardaste el archivo.
4. Ejecuta el siguiente comando:

```bash
python cafeteria.py
```

> **Nota importante:** La primera vez que ejecutes el programa, se creará automáticamente un archivo llamado `catalogo.db` en la misma carpeta. Este archivo es tu base de datos; si lo borras, perderás el registro de tus productos.

## 📖 Guía Rápida de Uso

1. **Agregar un producto:** Rellena los tres campos de texto superiores (Producto, Stock, Precio) y haz clic en el botón **Guardar**.
2. **Editar un producto:** Haz clic en cualquier elemento de la lista inferior. Sus datos se cargarán automáticamente en los campos de texto. Edita lo que necesites y presiona **Actualizar**.
3. **Borrar un producto:** Selecciona un producto de la lista inferior y haz clic en **Eliminar**. Acepta el cuadro de diálogo de confirmación para completar la acción.

---
*Desarrollado como ejemplo práctico de integración entre interfaces gráficas y bases de datos relacionales en Python.*
