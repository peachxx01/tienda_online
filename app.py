from flask import Flask, render_template, flash, request, redirect
import os
#from werkzeug.exceptions import RequestEntityTooLarge
#from datetime import timedelta
#from models.db import db
#from models.usuario import Usuario
#from models.producto import Producto
#from models.carrito import Carrito
#from models.carritoItem import CarritoItem
#from models.pedido import Pedido
#from models.pedidoItem import PedidoItem
#from models.categoria import Categoria
#from routes.routes_categorias import routes_categorias
#from routes.routes_productos import routes_productos
#from routes.routes_auth import routes_auth
#from routes.routes_user import routes_user
#from routes.routes_admin import routes_admin
#from routes.routes_carrito import routes_carrito
#from routes.routes_checkout import routes_checkout

import config.config as config

app = Flask(__name__)

app.config.from_object(config)


#db.init_app(app)

#with app.app_context():
    #db.drop_all()
    #db.create_all()
   

#Filtro de horas para cambiar las utc a horario argentino
"""@app.template_filter('fecha_ar')
def fecha_ar(fecha):
    if fecha:
        fecha_local = fecha - timedelta(hours=3)
        return fecha_local.strftime('%d/%m/%Y a las %H:%M hs')
    return ""


#Pasa las categorias al layout siempre, si no tendria que pasar las categorias por cada html que se extienda de layout
@app.context_processor
def inject_categorias():
    # Si la petición es para un archivo estático, no busques en la DB
    if request.endpoint == 'static':
        return {}
    return {
        'categorias': Categoria.query.all()
    }

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    flash("La imagen supera el tamaño máximo permitido (2MB)", "error")
    return redirect(request.referrer)

@app.route('/', methods=['GET'])
def home():
    productos_populares = Producto.query.filter_by(popular=True,activo=True).all()

    return render_template(
        'index.html',
        productos_populares=productos_populares
    )

app.register_blueprint(routes_categorias)
app.register_blueprint(routes_productos)
app.register_blueprint(routes_auth)
app.register_blueprint(routes_user)
app.register_blueprint(routes_admin)
app.register_blueprint(routes_carrito)
app.register_blueprint(routes_checkout)

"""
@app.route('/health')
def health():
    return "App viva", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)