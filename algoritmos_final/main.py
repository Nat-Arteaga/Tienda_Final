from producto import Producto
from pila import Pila
from cola import Cola
from arbol import InventarioArbol  # Importando la clase del árbol
from grafo import Grafo
import csv

# --- INSTANCIACIÓN DE ESTRUCTURAS ---
inventario = InventarioArbol()
pila_acciones = Pila()
cola_pedidos = Cola()
grafo_rutas = Grafo()


def inicializar_datos():

    # Productos iniciales (ÁRBOL)
    inventario.insertar(Producto(101, "Leche Entera", 5.50, 10))
    inventario.insertar(Producto(205, "Pan Integral", 8.00, 5))
    inventario.insertar(Producto(503, "Manzanas", 12.50, 20))

    # Rutas iniciales (GRAFO)
    grafo_rutas.agregar_arista("Almacen_A", "Zona_Norte", 15)
    grafo_rutas.agregar_arista("Almacen_A", "Zona_Centro", 10)
    grafo_rutas.agregar_arista("Zona_Norte", "Zona_Sur", 30)
    grafo_rutas.agregar_arista("Zona_Centro", "Zona_Sur", 12)
    grafo_rutas.agregar_arista("Zona_Centro", "Almacen_B", 5)

    pila_acciones.apilar({'tipo': 'INSERCION_INICIAL', 'id': 503})


# --- FUNCIONES CRUD y Exportar ---

def funcion_agregar_producto():
    print("\n--- AGREGAR NUEVO PRODUCTO ---")
    try:
        id_p = int(input("Ingrese ID del nuevo producto: "))
        nombre = input("Ingrese Nombre del producto: ")
        precio = float(input("Ingrese Precio: "))
        stock = int(input("Ingrese Stock inicial: "))
        nuevo_producto = Producto(id_p, nombre, precio, stock)
        inventario.insertar(nuevo_producto)
        pila_acciones.apilar({'tipo': 'INSERCION', 'id': id_p})
        print(f"✅ Producto '{nombre}' (ID {id_p}) agregado/actualizado correctamente.")
    except ValueError:
        print("❌ Error: El ID, Precio y Stock deben ser valores numéricos.")


def funcion_buscar(id_producto):
    producto = inventario.buscar(id_producto)
    if producto:
        print(f"\n🔍 Producto encontrado: {producto}")
    else:
        print(f"\n❌ Producto con ID {id_producto} no encontrado.")
    return producto


def funcion_eliminar(id_producto):
    producto = inventario.buscar(id_producto)
    if producto is None:
        print(f"\n❌ Producto con ID {id_producto} no existe para ser eliminado.")
        return False
    inventario.eliminar(id_producto)
    print(f"\n🗑️ Producto ID {id_producto} ({producto.nombre}) ELIMINADO del inventario.")
    pila_acciones.apilar({'tipo': 'ELIMINACION', 'id': id_producto, 'producto': producto})
    return True


def funcion_exportar():
    productos = inventario.obtener_todos_los_productos()
    nombre_archivo = 'inventario_exportado.csv'
    if not productos:
        print("⚠️ El inventario está vacío. Nada que exportar.")
        return
    try:
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
            campos = ['ID', 'Nombre', 'Precio', 'Stock']
            escritor = csv.writer(archivo_csv, delimiter=';')
            escritor.writerow(campos)
            for p in productos:
                escritor.writerow([p.id_producto, p.nombre, p.precio, p.stock])
        print(f"\n💾 Éxito: Inventario exportado a '{nombre_archivo}'.")
        print(f"Total de {len(productos)} productos exportados.")
    except Exception as e:
        print(f"\n❌ Error al exportar: {e}")



# --- MAS FUNCIONES ---

def realizar_venta(id_producto, cantidad):
    producto = inventario.buscar(id_producto)
    if producto is None or producto.stock < cantidad:
        print("❌ Venta fallida (Producto no encontrado o stock insuficiente).")
        return
    producto.stock -= cantidad
    print(f"✅ Venta realizada: {cantidad} unidades de {producto.nombre}.")
    accion_reversa = {'tipo': 'VENTA', 'id': id_producto, 'cantidad': cantidad}
    pila_acciones.apilar(accion_reversa)
    pedido = f"Pedido Venta: ID {id_producto}, Cantidad: {cantidad}"
    cola_pedidos.encolar(pedido)
    print(f"🚚 Pedido encolado para procesamiento logístico.")


def deshacer_ultima_accion():
    accion = pila_acciones.desapilar()
    if accion is None:
        print("❌ No hay acciones para deshacer.")
        return
    if accion['tipo'] == 'VENTA':
        producto = inventario.buscar(accion['id'])
        if producto:
            producto.stock += accion['cantidad']
            print(f"⏪ UNDO: Venta de {accion['cantidad']} de {producto.nombre} revertida. Stock restaurado.")
    elif accion['tipo'] == 'ELIMINACION':
        p_reinsertar = accion['producto']
        inventario.insertar(p_reinsertar)
        print(
            f"⏪ UNDO: Eliminación de {p_reinsertar.nombre} (ID {p_reinsertar.id_producto}) revertida. Producto restaurado.")
    elif accion['tipo'] == 'INSERCION' or accion['tipo'] == 'INSERCION_INICIAL':
        print("⚠️ UNDO: Las acciones de Inserción deben revertirse manualmente con la opción Eliminar.")


def procesar_pedido():
    pedido = cola_pedidos.desencolar()
    if pedido:
        print(f"📦 Procesando y enviando el pedido más antiguo: {pedido}")
    else:
        print("✅ No hay pedidos pendientes en la cola.")


def calcular_ruta_optima(origen, destino):
    ruta, costo = grafo_rutas.dijkstra(origen, destino)
    if ruta and costo != float('inf'):
        print(f"\n🗺️ Ruta más corta de **{origen}** a **{destino}** (Tiempo: **{costo}** min):")
        print(" -> ".join(ruta))
    else:
        print(f"❌ No se encontró una ruta de {origen} a {destino}.")


# --- MENÚ PRINCIPAL ---
def menu():
    while True:
        print("\n" + "=" * 50)
        print("      SISTEMA DE TIENDA                ")
        print("=" * 50)
        print("1. 🌳 Mostrar Inventario (Árbol)")
        print("2. ➕ Agregar Nuevo Producto (Árbol)")
        print("3. 🔍 Buscar Producto por ID (Árbol)")
        print("4. 🗑️ Eliminar Producto por ID (Árbol)")
        print("5. 🛒 Realizar Venta (Árbol, Pila, Cola)")
        print("6. ⏪ Deshacer Última Acción (Pila)")
        print("7. 📦 Procesar Siguiente Pedido (Cola)")
        print("8. 🌐 Calcular Ruta Óptima (Grafo)")
        print("9. 💾 Exportar Inventario a CSV")
        print("0. Salir")
        print("-" * 50)

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == '1':
                inventario.mostrar_inventario()
            elif opcion == '2':
                funcion_agregar_producto()
            elif opcion == '3':
                id_p = int(input("Ingrese el ID del producto a buscar: "))
                funcion_buscar(id_p)
            elif opcion == '4':
                id_p = int(input("Ingrese el ID del producto a eliminar: "))
                funcion_eliminar(id_p)
            elif opcion == '5':
                id_p = int(input("ID del producto a vender: "))
                cant = int(input("Cantidad a vender: "))
                realizar_venta(id_p, cant)
            elif opcion == '6':
                deshacer_ultima_accion()
            elif opcion == '7':
                procesar_pedido()
            elif opcion == '8':
                zonas = grafo_rutas.grafo.keys()
                print("\nZonas/Almacenes disponibles: " + ", ".join(zonas))
                origen = input("Origen: ")
                destino = input("Destino: ")
                if origen in zonas and destino in zonas:
                    calcular_ruta_optima(origen, destino)
                else:
                    print("⚠️ Asegúrese de que el origen y destino estén en la lista de zonas disponibles.")
            elif opcion == '9':
                funcion_exportar()
            elif opcion == '0':
                print("Saliendo del sistema.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
        except ValueError:
            print("Entrada inválida. Asegúrese de ingresar números correctos para ID, Precio o Cantidad.")


# --- (main) ---
if __name__ == "__main__":
    inicializar_datos()
    menu()