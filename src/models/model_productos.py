
from src.config.mysql_connection import get_mysql_connection

class Producto:

  @staticmethod
  def _asegurar_columna_categoria(connection):
    with connection.cursor() as cursor:
      cursor.execute(
        """
        SELECT COUNT(*) AS existe
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'producto'
          AND COLUMN_NAME = 'idcategoria'
        """
      )
      existe = cursor.fetchone()["existe"]

      if existe == 0:
        cursor.execute("ALTER TABLE producto ADD COLUMN idcategoria INT NULL")
        connection.commit()

  @staticmethod
  def leer_productos():
    connection = get_mysql_connection()
    Producto._asegurar_columna_categoria(connection)
    with connection.cursor() as cursor:
      cursor.execute(
        """
        SELECT
          p.idproducto,
          p.producto,
          p.marca,
          p.precio,
          p.idcategoria,
          c.categoria AS categoria_nombre
        FROM producto AS p
        LEFT JOIN categoria AS c ON c.idcategoria = p.idcategoria
        ORDER BY p.idproducto DESC
        """
      )
      datos = cursor.fetchall()
    connection.close()

    return datos

  @staticmethod
  def crear_producto(producto, marca, precio, idcategoria):
    connection = get_mysql_connection()
    Producto._asegurar_columna_categoria(connection)
    with connection.cursor() as cursor:
      cursor.execute(
        "INSERT INTO producto (producto, marca, precio, idcategoria) VALUES (%s, %s, %s, %s)",
        (producto, marca, precio, idcategoria)
      )
      connection.commit()
    connection.close()

  @staticmethod
  def actualizar_producto(idproducto, producto, marca, precio, idcategoria):
    connection = get_mysql_connection()
    Producto._asegurar_columna_categoria(connection)
    with connection.cursor() as cursor:
      cursor.execute(
        "UPDATE producto SET producto=%s, marca=%s, precio=%s, idcategoria=%s WHERE idproducto=%s",
        (producto, marca, precio, idcategoria, idproducto)
      )
      connection.commit()
    connection.close()

  @staticmethod
  def eliminar_producto(idproducto):
    connection = get_mysql_connection()
    with connection.cursor() as cursor:
      cursor.execute("DELETE FROM producto WHERE idproducto=%s", (idproducto,))
      connection.commit()
    connection.close()

  @staticmethod
  def obtener_producto_por_id(idproducto):
    connection = get_mysql_connection()
    with connection.cursor() as cursor:
      cursor.execute(
        "SELECT idproducto, producto FROM producto WHERE idproducto=%s",
        (idproducto,)
      )
      dato = cursor.fetchone()
    connection.close()

    return dato