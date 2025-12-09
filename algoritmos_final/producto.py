# Estructura de datos del producto

class Producto:
    def __init__(self, id_producto, nombre, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return f"ID: {self.id_producto} | Nombre: {self.nombre} | Precio: ${self.precio:.2f} | Stock: {self.stock}"

    def __lt__(self, other):
        return self.id_producto < other.id_producto