import os
import shutil
from datetime import datetime

# --- Funciones para manejar productos ---
def parse_line(linea, prod_id):
    """
    Convierte una línea del archivo inventario.txt en un diccionario de producto.
    Formato esperado: Nombre, 15 USD, 50 unidades, M
    """
    partes = [p.strip() for p in linea.split(',')]
    nombre = partes[0] if len(partes) > 0 else ''
    precio = partes[1] if len(partes) > 1 else '0 USD'
    unidades = partes[2] if len(partes) > 2 else '0 unidades'
    talla = partes[3] if len(partes) > 3 else ''
    return {'id': prod_id, 'nombre': nombre, 'precio': precio, 'unidades': unidades, 'talla': talla}

def format_product(producto):
    """Convierte el diccionario de producto a la línea que va en inventario.txt (con \n)."""
    return f"{producto.get('nombre','')}, {producto.get('precio','')}, {producto.get('unidades','')}, {producto.get('talla','')}\n"

def product_str(producto):
    """Representación legible del producto para imprimir en consola."""
    return f"Producto(ID: {producto.get('id')}, Nombre: {producto.get('nombre')}, Precio: {producto.get('precio')}, Unidades: {producto.get('unidades')}, Talla: {producto.get('talla')})"

# --- Funciones para manejar el inventario ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTARIO_FILE = os.path.join(BASE_DIR, 'inventario.txt')

def cargar_inventario(path=INVENTARIO_FILE):
    """
    Carga el inventario desde un archivo de texto y devuelve una lista de Producto.
    """
    products = []
    if not os.path.exists(path):
        return products
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        prod = parse_line(line, i + 1)
        products.append(prod)
    return products


def guardar_inventario(products, path=INVENTARIO_FILE):
    """
    Guarda la lista de productos en el archivo de inventario (sobrescribe).
    """
    with open(path, 'w', encoding='utf-8') as f:
        for p in products:
            f.write(format_product(p))


def backup_inventario(path=INVENTARIO_FILE):
    """Crea una copia de seguridad del archivo de inventario con timestamp y devuelve la ruta."""
    if not os.path.exists(path):
        return None
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    base, ext = os.path.splitext(path)
    dst = f"{base}_backup_{ts}{ext}"
    shutil.copy2(path, dst)
    return dst


def info_archivo(path=INVENTARIO_FILE):
    """Devuelve tamaño y fecha de última modificación del archivo."""
    if not os.path.exists(path):
        return None
    size = os.path.getsize(path)
    mtime = os.path.getmtime(path)
    return {'size': size, 'mtime': mtime}

def imprimir_inventario(products):
    """
    Imprime el inventario en la consola.
    """
    if not products:
        print('Inventario vacío.')
        return
    for p in products:
        print(product_str(p))

def menu():
    print("\n--- Menú ---")
    print("1. Cargar inventario")
    print("2. Agregar producto (append)")
    print("3. Buscar producto (por ID o nombre)")
    print("4. Modificar producto (por ID)")
    print("5. Eliminar producto (por ID)")
    print("6. Hacer backup")
    print("7. Mostrar info del archivo")
    print("0. Salir")

def main():
    products = []
    while True:
        menu()
        opcion = input('Seleccione una opción: ')
        if opcion == '1':
            print('Cargando inventario...')
            products = cargar_inventario()
            print('\nInventario inicial:')
            imprimir_inventario(products)
        elif opcion == '2':
            # Agregar en modo append directamente al archivo
            print('Agregando producto (append)...')
            nombre = input('Nombre: ')
            precio = input('Precio: ')
            unidades = input('Unidades: ')
            talla = input('Talla: ')
            # Crear dict del producto con id siguiente
            products = cargar_inventario()
            new_id = len(products) + 1
            nuevo_producto = {'id': new_id, 'nombre': nombre, 'precio': precio, 'unidades': unidades, 'talla': talla}
            with open(INVENTARIO_FILE, 'a', encoding='utf-8') as f:
                f.write(format_product(nuevo_producto))
            print('Producto agregado (append).')
        elif opcion == '3':
            term = input('Ingrese ID o parte del nombre para buscar: ')
            products = cargar_inventario()
            results = []
            if term.isdigit():
                tid = int(term)
                results = [p for p in products if p['id'] == tid]
            else:
                results = [p for p in products if term.lower() in p['nombre'].lower()]
            if not results:
                print('No se encontraron productos.')
            else:
                for r in results:
                    print(product_str(r))
        elif opcion == '4':
            # Modificar producto por ID
            pid = input('ID del producto a modificar: ')
            if not pid.isdigit():
                print('ID inválido.')
                continue
            pid = int(pid)
            while True:
                products = cargar_inventario()
                p = next((x for x in products if x['id'] == pid), None)
                if not p:
                    print('Producto no encontrado.')
                    break
                print('Modificando el siguiente producto:', product_str(p))
                print ("elija que caracteristica cambiar")
                print ("1. nombre")
                print ("2. precio")
                print ("3. unidades")
                print ("4. talla")
                print ("5. salir")
                opcion_mod = input('Seleccione una opción: ')
                if opcion_mod == '1':
                    nuevo_nombre = input('Nuevo nombre: ')
                    for prod in products:
                        if prod['id'] == pid:
                            prod['nombre'] = nuevo_nombre
                            break
                    guardar_inventario(products)
                    print('Nombre modificado y guardado.')
                elif opcion_mod == '2':
                    nuevo_precio = input('Nuevo precio: ')
                    for prod in products:
                        if prod['id'] == pid:
                            prod['precio'] = nuevo_precio
                            break
                    guardar_inventario(products)
                    print('Precio modificado y guardado.')
                elif opcion_mod == '3':
                    nuevas_unidades = input('Nuevas unidades: ')
                    for prod in products:
                        if prod['id'] == pid:
                            prod['unidades'] = nuevas_unidades
                            break
                    guardar_inventario(products)
                    print('Unidades modificadas y guardadas.')
                elif opcion_mod == '4':
                    nueva_talla = input('Nueva talla: ')
                    for prod in products:
                        if prod['id'] == pid:
                            prod['talla'] = nueva_talla
                            break
                    guardar_inventario(products)
                    print('Talla modificada y guardada.')
                elif opcion_mod == '5':
                    print('Saliendo de la modificación.')
                    break
                else:
                    print('Opción no válida.')
        elif opcion == '5':
            pid = input('ID del producto a eliminar: ')
            if not pid.isdigit():
                print('ID inválido.')
                continue
            pid = int(pid)
            products = cargar_inventario()
            new_list = [p for p in products if p['id'] != pid]
            if len(new_list) == len(products):
                print('Producto no encontrado.')
            else:
                # Reasignar IDs secuenciales
                for idx, p in enumerate(new_list, start=1):
                    p['id'] = idx
                guardar_inventario(new_list)
                print('Producto eliminado y archivo actualizado.')
        elif opcion == '6':
            print('Creando copia de seguridad...')
            dst = backup_inventario()
            if dst:
                print('Copia creada en:', dst)
            else:
                print('No existe el archivo a respaldar.')
        elif opcion == '7':
            info = info_archivo()
            if not info:
                print('Archivo no encontrado.')
            else:
                print(f"Tamaño: {info['size']} bytes")
                print('Última mod.:', datetime.fromtimestamp(info['mtime']))
        elif opcion == '0':
            print('Saliendo...')
            break
        else:
            print('Opción no válida. Intente de nuevo.')

if __name__ == "__main__":
    main()
