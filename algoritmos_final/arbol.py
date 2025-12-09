# Árbol Binario de Búsqueda (ABB) para el Inventario


class NodoArbol:  # Nombre de la clase del nodo
    def __init__(self, producto):
        self.producto = producto
        self.izquierda = None
        self.derecha = None


class InventarioArbol:  # Nombre de la clase principal
    def __init__(self):
        self.raiz = None
    # ---AGREGAR---
    def _insertar_recursivo(self, raiz, producto):
        if raiz is None:
            return NodoArbol(producto)
        if producto.id_producto < raiz.producto.id_producto:
            raiz.izquierda = self._insertar_recursivo(raiz.izquierda, producto)
        elif producto.id_producto > raiz.producto.id_producto:
            raiz.derecha = self._insertar_recursivo(raiz.derecha, producto)
        else:
            # Actualización de stock si el ID existe
            raiz.producto.stock += producto.stock
            print(f"Producto {producto.id_producto} actualizado. Nuevo stock: {raiz.producto.stock}")
        return raiz
    def insertar(self, producto):
        self.raiz = self._insertar_recursivo(self.raiz, producto)

    # ---BÚSQUEDA---
    def _buscar_recursivo(self, raiz, id_producto):
        if raiz is None or raiz.producto.id_producto == id_producto:
            return raiz.producto if raiz else None
        if id_producto < raiz.producto.id_producto:
            return self._buscar_recursivo(raiz.izquierda, id_producto)
        else:
            return self._buscar_recursivo(raiz.derecha, id_producto)
    def buscar(self, id_producto):
        return self._buscar_recursivo(self.raiz, id_producto)

    # ---ELIMINACIÓN---
    def _encontrar_minimo(self, nodo):
        """in-orden."""
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual
    def _eliminar_recursivo(self, raiz, id_producto):
        if raiz is None:
            return raiz
        if id_producto < raiz.producto.id_producto:
            raiz.izquierda = self._eliminar_recursivo(raiz.izquierda, id_producto)
        elif id_producto > raiz.producto.id_producto:
            raiz.derecha = self._eliminar_recursivo(raiz.derecha, id_producto)
        else:
            if raiz.izquierda is None:
                temp = raiz.derecha
                raiz = None
                return temp
            elif raiz.derecha is None:
                temp = raiz.izquierda
                raiz = None
                return temp
            temp = self._encontrar_minimo(raiz.derecha)
            raiz.producto = temp.producto
            raiz.derecha = self._eliminar_recursivo(raiz.derecha, temp.producto.id_producto)
        return raiz
    def eliminar(self, id_producto):
        self.raiz = self._eliminar_recursivo(self.raiz, id_producto)
        return self.raiz is not None

        # ---EXPORTAR---
    def _recorrido_inorden(self, raiz, lista_productos):
        if raiz:
            self._recorrido_inorden(raiz.izquierda, lista_productos)
            lista_productos.append(raiz.producto)
            self._recorrido_inorden(raiz.derecha, lista_productos)
        return lista_productos
    def obtener_todos_los_productos(self):
        return self._recorrido_inorden(self.raiz, [])
    def mostrar_inventario(self):
        print("\n--- INVENTARIO (Ordenado por ID) ---")
        productos = self.obtener_todos_los_productos()
        if not productos:
            print("Inventario vacío.")
        else:
            for p in productos:
                print(p)
        print("-----------------------------------")