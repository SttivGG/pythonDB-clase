
from datetime import datetime

from bson import ObjectId

from src.config.mongo_connection import get_mongo_connection

class ImagenProducto:

  @staticmethod
  def _normalizar_fecha(fecha_subida):
    if not fecha_subida:
      return datetime.now()
    return datetime.fromisoformat(fecha_subida)

  @staticmethod
  def leer_imagenes():
    db = get_mongo_connection()
    imagenes = list(db.producto.find().sort("fecha_subida", -1))
    for imagen in imagenes:
      imagen["mongo_id"] = str(imagen.pop("_id"))
    return imagenes

  @staticmethod
  def crear_imagen(idproducto, producto, url, descripcion, fecha_subida):
    db = get_mongo_connection()
    db.producto.insert_one({
      "idproducto": int(idproducto),
      "producto": producto,
      "url": url,
      "descripcion": descripcion,
      "fecha_subida": ImagenProducto._normalizar_fecha(fecha_subida)
    })

  @staticmethod
  def actualizar_imagen(mongo_id, idproducto, producto, url, descripcion, fecha_subida):
    db = get_mongo_connection()
    db.producto.update_one(
      {"_id": ObjectId(mongo_id)},
      {
        "$set": {
          "idproducto": int(idproducto),
          "producto": producto,
          "url": url,
          "descripcion": descripcion,
          "fecha_subida": ImagenProducto._normalizar_fecha(fecha_subida)
        }
      }
    )

  @staticmethod
  def eliminar_imagen(mongo_id):
    db = get_mongo_connection()
    db.producto.delete_one({"_id": ObjectId(mongo_id)})