from faker import Faker
import psycopg2
from psycopg2 import sql
import random

# Configuración de conexión a la base de datos
dbname = "grupo1db"
user = "postgres"
password = "grupo1"
host = "10.10.10.2"
port = "13405"


# Función para generar datos ficticios y llenar las tablas
def generate_fake_data():
    fake = Faker(['es_ES'])

    # Conexión a la base de datos
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    # Llenar la tabla Cliente
    for _ in range(200):
        nombre = fake.first_name()[:20]  # Limitar el nombre a 20 caracteres
        apellido = fake.last_name()[:20]  # Limitar el apellido a 20 caracteres
        direccion = fake.address()[:100]  # Limitar la dirección a 100 caracteres
        telefono = fake.numerify(text='##########')[:10]  # Limitar el teléfono a 10 caracteres
        email = fake.email()[:30]  # Limitar el email a 30 caracteres
        pais = fake.country()[:100]  # Limitar el país a 100 caracteres
        cursor.execute(sql.SQL(
            "INSERT INTO Cliente (nombre, apellido, direccion, telefono, email, pais) VALUES (%s, %s, %s, %s, %s, %s)"),
                       (nombre, apellido, direccion, telefono, email, pais))
    conn.commit()

    # Llenar la tabla Empleado
    for _ in range(200):
        nombre = fake.first_name()[:20]  # Limitar el nombre a 20 caracteres
        apellido = fake.last_name()[:20]  # Limitar el apellido a 20 caracteres
        cargo = fake.job()[:20]  # Limitar el cargo a 20 caracteres
        fecha_contratacion = fake.date_between(start_date='-5y', end_date='today')
        cursor.execute(
            sql.SQL("INSERT INTO Empleado (nombre, apellido, cargo, fecha_contratacion) VALUES (%s, %s, %s, %s)"),
            (nombre, apellido, cargo, fecha_contratacion))
    conn.commit()

    # Llenar la tabla Entrega
    for _ in range(200):
        metodo_entrega = fake.random_element(elements=('Correo', 'Mensajería', 'Transporte público'))[:50]  # Limitar a 50 caracteres
        descripcion = fake.text(max_nb_chars=200)
        cursor.execute(sql.SQL("INSERT INTO Entrega (metodo_entrega, descripcion) VALUES (%s, %s)"),
                       (metodo_entrega, descripcion[:200]))  # Limitar a 200 caracteres
    conn.commit()

    # Llenar la tabla Pedido
    for _ in range(200):
        # Obtener un cliente_id existente en la tabla Cliente
        cursor.execute("SELECT cliente_id FROM Cliente ORDER BY random() LIMIT 1")
        cliente_id = cursor.fetchone()[0]

        empleado_id = fake.random_int(min=1, max=200)
        entrega_id = fake.random_int(min=1, max=200)
        fecha_pedido = fake.date_between(start_date='-1y', end_date='today')
        fecha_envio = fake.date_between(start_date='-1y', end_date='today')
        estado = fake.random_element(elements=('Pendiente', 'En proceso', 'Entregado'))[:30]  # Limitar a 30 caracteres

        cursor.execute(sql.SQL(
            "INSERT INTO Pedido (cliente_id, empleado_id, entrega_id, fecha_pedido, fecha_envio, estado) VALUES (%s, %s, %s, %s, %s, %s)"),
            (cliente_id, empleado_id, entrega_id, fecha_pedido, fecha_envio, estado))
    conn.commit()

    # Llenar la tabla Proveedor
    for _ in range(200):
        nombre = fake.company()[:20]  # Limitar a 20 caracteres
        direccion = fake.address()[:100]  # Limitar a 100 caracteres
        telefono = fake.numerify(text='##########')[:10]  # Limitar a 10 caracteres
        email = fake.email()[:80]  # Limitar a 80 caracteres

        cursor.execute(sql.SQL("INSERT INTO Proveedor (nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s)"),
                       (nombre, direccion, telefono, email))
    conn.commit()

    # Llenar la tabla Flor
    for _ in range(200):
        proveedor_id = fake.random_int(min=1, max=200)
        nombre = fake.word()[:20]  # Limitar a 20 caracteres
        especie = fake.word()[:20]  # Limitar a 20 caracteres
        color = fake.color_name()[:20]  # Limitar a 20 caracteres
        precio_unitario = round(random.uniform(1.0, 100.0), 2)
        descripcion = fake.text(max_nb_chars=200)[:200]  # Limitar a 200 caracteres

        cursor.execute(sql.SQL(
            "INSERT INTO Flor (proveedor_id, nombre, especie, color, precio_unitario, descripcion) VALUES (%s, %s, %s, %s, %s, %s)"),
            (proveedor_id, nombre, especie, color, precio_unitario, descripcion))
    conn.commit()

    # Llenar la tabla Cultivo
    for _ in range(200):
        fecha_siembra = fake.date_between(start_date='-5y', end_date='today')
        fecha_cosecha = fake.date_between(start_date='-5y', end_date='today')
        cantidad_cosechada = fake.random_int(min=100, max=1000)

        try:
            cursor.execute(
                sql.SQL("INSERT INTO Cultivo (fecha_siembra, fecha_cosecha, cantidad_cosechada) VALUES (%s, %s, %s)"),
                (fecha_siembra, fecha_cosecha, cantidad_cosechada))
        except psycopg2.IntegrityError as e:
            conn.rollback()  # Rollback en caso de error de integridad (por ejemplo, fechas duplicadas)
            print(f"Error al insertar en Cultivo: {e}")

    conn.commit()

    # Llenar la tabla Lote
    for _ in range(200):
        nombre = fake.word()[:30]  # Limitar el nombre a 30 caracteres
        numero_lote = fake.random_int(min=1, max=200)
        tamano = round(random.uniform(1.0, 100.0), 2)  # Generar decimal entre 1.0 y 100.0 con 2 decimales
        tipo = fake.word()[:30]  # Limitar el tipo a 30 caracteres

        try:
            cursor.execute(
                sql.SQL("INSERT INTO Lote (nombre, numero_lote, tamano, tipo) VALUES (%s, %s, %s, %s)"),
                (nombre, numero_lote, tamano, tipo))
        except psycopg2.IntegrityError as e:
            conn.rollback()  # Rollback en caso de error de integridad (por ejemplo, nombre y número de lote duplicados)
            print(f"Error al insertar en Lote: {e}")

    conn.commit()

    # Llenar la tabla CultivoLote
    for cultivo_id in range(1, 201):  # suponiendo que tenemos 200 cultivos creados
        lote_id = fake.random_int(min=1, max=200)

        try:
            cursor.execute(
                sql.SQL("INSERT INTO CultivoLote (cultivo_id, lote_id) VALUES (%s, %s)"),
                (cultivo_id, lote_id)
            )
        except psycopg2.IntegrityError as e:
            conn.rollback()  # Rollback en caso de error de integridad
            print(f"Error al insertar en CultivoLote: {e}")

    conn.commit()

    # Llenar la tabla LoteFlor
    for lote_id in range(1, 201):  # suponiendo que tenemos 200 lotes creados
        flor_id = fake.random_int(min=1, max=200)

        try:
            cursor.execute(
                sql.SQL("INSERT INTO LoteFlor (lote_id, flor_id) VALUES (%s, %s)"),
                (lote_id, flor_id)
            )
        except psycopg2.IntegrityError as e:
            conn.rollback()  # Rollback en caso de error de integridad
            print(f"Error al insertar en LoteFlor: {e}")

    conn.commit()

    # Llenar la tabla FlorPedido
    for pedido_id in range(1, 201):  # suponiendo que tenemos 200 pedidos creados
        flor_id = fake.random_int(min=1, max=200)
        cantidad = fake.random_int(min=1, max=20)

        try:
            cursor.execute(
                sql.SQL("INSERT INTO FlorPedido (pedido_id, flor_id, cantidad) VALUES (%s, %s, %s)"),
                (pedido_id, flor_id, cantidad)
            )
        except psycopg2.IntegrityError as e:
            conn.rollback()  # Rollback en caso de error de integridad
            print(f"Error al insertar en FlorPedido: {e}")

    conn.commit()

    # Cerrar conexión a la base de datos
    cursor.close()
    conn.close()


if __name__ == "__main__":
    generate_fake_data()
