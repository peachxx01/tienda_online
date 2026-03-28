from flask import Blueprint, request, render_template
from sqlalchemy import or_
from models.categoria import Categoria
from models.producto import Producto

routes_productos=Blueprint('routes_productos', __name__, url_prefix=('/productos'))

@routes_productos.route('/buscar')
def buscar():
    q = request.args.get('q', '').strip()

    productos = []
    if q:
        productos = (
            Producto.query
            .join(Categoria)
            .filter(
                Producto.activo == True,
                or_(
                    Producto.nombre.ilike(f"%{q}%"),
                    Categoria.nombre.ilike(f"%{q}%")
                )
            ).limit(20).all()
        )

    return render_template(
        'productos/resultados_busqueda.html',
        productos=productos,
        q=q
    )

@routes_productos.route('/detalle/<int:id_producto>')
def detalle_producto(id_producto):
    producto = Producto.query.filter_by(id_producto=id_producto,activo=True).first_or_404()

    return render_template('productos/detalle.html', producto=producto)