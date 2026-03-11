from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from src.models.model_productos import Producto
from src.models.model_imagenes import ImagenProducto
from src.models.model_categorias import Categoria




productos_c = Blueprint(
  'productos_c',__name__,template_folder='../templates'
)


def _sql_base_completa():
  productos = Producto.leer_productos()
  categorias = Categoria.leer_categorias()
  return bool(productos) and bool(categorias), productos, categorias


@productos_c.route("/productos")
def obtener_productos():
  _, data, categorias = _sql_base_completa()
  requiere_sql = request.args.get("requiere_sql") == "1"
  producto_incompleto = request.args.get("producto_incompleto") == "1"
  return render_template(
    "productos.html",
    data=data,
    categorias=categorias,
    requiere_sql=requiere_sql,
    producto_incompleto=producto_incompleto
  )


@productos_c.route("/productos/crear", methods=["POST"])
def crear_producto():
  producto = request.form.get("producto", "").strip()
  marca = request.form.get("marca", "").strip()
  precio = request.form.get("precio", "").strip()
  idcategoria = request.form.get("idcategoria", "").strip()

  if producto and marca and precio and idcategoria:
    Producto.crear_producto(producto, marca, precio, idcategoria)
    return redirect(url_for("productos_c.obtener_imagenes"))

  return redirect(url_for("productos_c.obtener_productos", producto_incompleto=1))


@productos_c.route("/productos/editar/<int:idproducto>", methods=["POST"])
def editar_producto(idproducto):
  producto = request.form.get("producto", "").strip()
  marca = request.form.get("marca", "").strip()
  precio = request.form.get("precio", "").strip()
  idcategoria = request.form.get("idcategoria", "").strip()

  if producto and marca and precio and idcategoria:
    Producto.actualizar_producto(idproducto, producto, marca, precio, idcategoria)

  return redirect(url_for("productos_c.obtener_productos"))


@productos_c.route("/productos/eliminar/<int:idproducto>", methods=["POST"])
def eliminar_producto(idproducto):
  Producto.eliminar_producto(idproducto)
  return redirect(url_for("productos_c.obtener_productos"))


@productos_c.route("/categorias/crear", methods=["POST"])
def crear_categoria():
  categoria = request.form.get("categoria", "").strip()
  descripcion = request.form.get("descripcion", "").strip()

  if categoria:
    Categoria.crear_categoria(categoria, descripcion)

  return redirect(url_for("productos_c.obtener_productos"))


@productos_c.route("/categorias/editar/<int:idcategoria>", methods=["POST"])
def editar_categoria(idcategoria):
  categoria = request.form.get("categoria", "").strip()
  descripcion = request.form.get("descripcion", "").strip()

  if categoria:
    Categoria.actualizar_categoria(idcategoria, categoria, descripcion)

  return redirect(url_for("productos_c.obtener_productos"))


@productos_c.route("/categorias/eliminar/<int:idcategoria>", methods=["POST"])
def eliminar_categoria(idcategoria):
  Categoria.eliminar_categoria(idcategoria)
  return redirect(url_for("productos_c.obtener_productos"))



@productos_c.route("/imagenes_productos")
def obtener_imagenes():
  sql_ok, _, _ = _sql_base_completa()
  if not sql_ok:
    return redirect(url_for("productos_c.obtener_productos", requiere_sql=1))

  data2 = ImagenProducto.leer_imagenes()
  productos = Producto.leer_productos()
  return render_template("imagenes_productos.html", data2=data2, productos=productos)


@productos_c.route("/imagenes_productos/crear", methods=["POST"])
def crear_imagen():
  idproducto = request.form.get("idproducto", "").strip()
  url = request.form.get("url", "").strip()
  descripcion = request.form.get("descripcion", "").strip()
  fecha_subida = request.form.get("fecha_subida", "").strip()
  producto = Producto.obtener_producto_por_id(idproducto) if idproducto else None

  if producto and url and descripcion:
    ImagenProducto.crear_imagen(idproducto, producto["producto"], url, descripcion, fecha_subida)

  return redirect(url_for("productos_c.obtener_imagenes"))


@productos_c.route("/imagenes_productos/editar/<mongo_id>", methods=["POST"])
def editar_imagen(mongo_id):
  idproducto = request.form.get("idproducto", "").strip()
  url = request.form.get("url", "").strip()
  descripcion = request.form.get("descripcion", "").strip()
  fecha_subida = request.form.get("fecha_subida", "").strip()
  producto = Producto.obtener_producto_por_id(idproducto) if idproducto else None

  if producto and url and descripcion:
    ImagenProducto.actualizar_imagen(mongo_id, idproducto, producto["producto"], url, descripcion, fecha_subida)

  return redirect(url_for("productos_c.obtener_imagenes"))


@productos_c.route("/imagenes_productos/eliminar/<mongo_id>", methods=["POST"])
def eliminar_imagen(mongo_id):
  ImagenProducto.eliminar_imagen(mongo_id)
  return redirect(url_for("productos_c.obtener_imagenes"))


@productos_c.route("/compilado_bd")
def compilado_bd():
  sql_ok, productos, _ = _sql_base_completa()
  if not sql_ok:
    return redirect(url_for("productos_c.obtener_productos", requiere_sql=1))

  imagenes = ImagenProducto.leer_imagenes()

  imagenes_por_producto = {}
  for imagen in imagenes:
    idproducto = imagen.get("idproducto")
    imagenes_por_producto.setdefault(idproducto, []).append(imagen)

  productos_por_id = {p["idproducto"]: p for p in productos}
  filas_compiladas = []

  for producto in productos:
    imgs = imagenes_por_producto.get(producto["idproducto"], [])
    if imgs:
      for imagen in imgs:
        filas_compiladas.append({
          "idproducto": producto["idproducto"],
          "producto": producto["producto"],
          "marca": producto["marca"],
          "categoria": producto.get("categoria_nombre"),
          "precio": producto["precio"],
          "mongo_id": imagen.get("mongo_id"),
          "url": imagen.get("url"),
          "descripcion": imagen.get("descripcion"),
          "fecha_subida": imagen.get("fecha_subida")
        })
    else:
      filas_compiladas.append({
        "idproducto": producto["idproducto"],
        "producto": producto["producto"],
        "marca": producto["marca"],
        "categoria": producto.get("categoria_nombre"),
        "precio": producto["precio"],
        "mongo_id": None,
        "url": None,
        "descripcion": None,
        "fecha_subida": None
      })

  for imagen in imagenes:
    if imagen.get("idproducto") not in productos_por_id:
      filas_compiladas.append({
        "idproducto": imagen.get("idproducto"),
        "producto": "Producto no existe en SQL",
        "marca": None,
        "categoria": None,
        "precio": None,
        "mongo_id": imagen.get("mongo_id"),
        "url": imagen.get("url"),
        "descripcion": imagen.get("descripcion"),
        "fecha_subida": imagen.get("fecha_subida")
      })

  filas_compiladas.sort(
    key=lambda fila: (
      fila.get("idproducto") if fila.get("idproducto") is not None else -1,
      fila.get("fecha_subida") or 0
    ),
    reverse=True
  )

  return render_template(
    "compilado_bd.html",
    filas_compiladas=filas_compiladas
  )