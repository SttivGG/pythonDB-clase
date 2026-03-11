from src.config.mysql_connection import get_mysql_connection


class Categoria:

  @staticmethod
  def leer_categorias():
    connection = get_mysql_connection()
    with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM categoria AS c ORDER BY c.idcategoria DESC")
      datos = cursor.fetchall()
    connection.close()

    return datos

  @staticmethod
  def crear_categoria(categoria, descripcion):
    connection = get_mysql_connection()
    with connection.cursor() as cursor:
      cursor.execute(
        "INSERT INTO categoria (categoria, descripcion) VALUES (%s, %s)",
        (categoria, descripcion)
      )
      connection.commit()
    connection.close()

  @staticmethod
  def actualizar_categoria(idcategoria, categoria, descripcion):
    connection = get_mysql_connection()
    with connection.cursor() as cursor:
      cursor.execute(
        "UPDATE categoria SET categoria=%s, descripcion=%s WHERE idcategoria=%s",
        (categoria, descripcion, idcategoria)
      )
      connection.commit()
    connection.close()

  @staticmethod
  def eliminar_categoria(idcategoria):
    connection = get_mysql_connection()
    with connection.cursor() as cursor:
      cursor.execute(
        "UPDATE producto SET idcategoria=NULL WHERE idcategoria=%s",
        (idcategoria,)
      )
      cursor.execute("DELETE FROM categoria WHERE idcategoria=%s", (idcategoria,))
      connection.commit()
    connection.close()
