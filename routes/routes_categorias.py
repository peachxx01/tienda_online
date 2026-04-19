from flask import Blueprint, render_template
from models.categoria import Categoria
from models.producto import Producto

routes_categorias = Blueprint('routes_categorias', __name__, url_prefix=('/categorias'))

#FILTRADO DE CATEGORIAS POR SLUG
@routes_categorias.route('/<slug>')
def productos_por_categoria(slug):
    categoria = Categoria.query.filter_by(slug=slug).first_or_404()

    productos = Producto.query.filter_by(categoria_id=categoria.id_categoria,activo=True).all()

    return render_template(
        'productos/productos_por_categoria.html',
        categoria=categoria,
        productos=productos
    )
