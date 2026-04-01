import cloudinary.uploader
from sqlalchemy import exists, and_
from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from models.db import db
from models.producto import Producto
from models.categoria import Categoria
from models.pedidoItem import PedidoItem
from models.pedido import Pedido
from utils.decorators import login_required, admin_required
from services.pedido_service import cambiar_estado_pedido

routes_admin=Blueprint('routes_admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@routes_admin.route('/panel')
@login_required
@admin_required
def panel():
    return render_template('admin/panel_admin.html')


@routes_admin.route('/stock')
@login_required
@admin_required
def inventario():

    categoria_id = request.args.get("categoria", type=int)

    query = Producto.query.filter_by(activo=True)

    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)

    productos = query.order_by(Producto.id_producto.desc()).all()

    categorias = Categoria.query.all()

    return render_template(
        'admin/stock.html',
        productos=productos,
        categorias=categorias
    )


@routes_admin.route('/borrar/<int:id_producto>', methods=['POST'])
@login_required
@admin_required
def borrar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)

    existe_bloqueante = db.session.query(
        exists().where(
            and_(
                PedidoItem.producto_id == id_producto,
                Pedido.id_pedido == PedidoItem.pedido_id,
                Pedido.estado.in_(["pendiente", "pagado"])
            )
        )
    ).scalar()

    if existe_bloqueante:
        flash(
            "No se puede eliminar el producto porque está en pedidos pendientes o ya pagados.",
            "danger"
        )
        return redirect(request.referrer)

    if producto.imagen:
        if producto.imagen_public_id:
            try:
                cloudinary.uploader.destroy(producto.imagen_public_id)
            except Exception as e:
                print("Error eliminando imagen:", e)

    #soft delete
    producto.activo = False
    db.session.commit()

    flash("Producto eliminado correctamente", "success")
    return redirect(url_for('routes_admin.inventario'))

@routes_admin.route('/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_producto():

    if request.method == 'POST':
        nombre= request.form.get('nombre')
        descripcion=request.form.get('descripcion')
        categoria_id=request.form.get('categoria_id')
        popular='popular' in request.form

        try:
            precio_venta=float(request.form.get('precio_venta'))
            precio_compra= float(request.form.get('precio_compra'))
            stock=int(request.form.get('stock'))
        except (ValueError, TypeError):
            flash("Datos numéricos inválidos", "error")
            return redirect(request.url)
        
        if precio_venta<0 or precio_compra<0:
            flash("Los precios no pueden ser negativos", "error")
            return redirect(request.url)
        
        if stock<0:
            flash("El stock no puede ser negativo", "error")
            return redirect(request.url)
        
        if stock>10000:
            flash("Cantidad muy grande de stock", "error")
            return redirect(request.url)

        if precio_venta<precio_compra:
            flash("El precio de venta no puede ser menos al de compra", "warning")
            return redirect(request.url)
        
        imagen_file=request.files.get('imagen')
        nombre_imagen= None
        imagen_public_id = None

        if imagen_file and imagen_file.filename != '':
            if allowed_file(imagen_file.filename):
                resultado = cloudinary.uploader.upload(imagen_file,folder="productos")
                nombre_imagen = resultado['secure_url']
                imagen_public_id = resultado['public_id']
            else:
                flash("Formato de imagen no permitido (solo jpg, jpeg, png)", "danger")
                return redirect(request.url)
        
        nuevo_producto=Producto(
            nombre=nombre,
            precio_venta=float(precio_venta),
            precio_compra=float(precio_compra),
            descripcion=descripcion,
            stock=int(stock),
            categoria_id=int(categoria_id),
            popular=popular,
            imagen=nombre_imagen,
            imagen_public_id=imagen_public_id
        )

        db.session.add(nuevo_producto)
        db.session.commit()

        flash ("Producto creado correctamente", "success")
        return redirect(url_for('routes_admin.panel'))
    
    categorias=Categoria.query.all()
    return render_template('admin/crear_producto.html', categorias=categorias)


@routes_admin.route('/editar/<int:id_producto>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_producto(id_producto):
    producto=Producto.query.get_or_404(id_producto)

    if request.method=='POST':
        producto.nombre= request.form.get('nombre')
        producto.descripcion= request.form.get('descripcion')
        producto.categoria_id=int(request.form.get('categoria_id'))
        producto.popular='popular' in request.form

        try:
            producto.precio_venta= float(request.form.get('precio_venta'))
            producto.precio_compra= float(request.form.get('precio_compra'))
            producto.stock=int(request.form.get('stock'))
        except (ValueError, TypeError):
            flash("Datos numéricos inválidos", "error")
            return redirect(request.url)
        
        if producto.precio_venta<0 or producto.precio_compra<0:
            flash("Los precios no pueden ser negativos", "error")
            return redirect(request.url)
        
        if producto.stock<0:
            flash("El stock no puede ser negativo", "error")
            return redirect(request.url)
        
        if producto.stock>10000:
            flash("Cantidad muy grande de stock", "error")
            return redirect(request.url)

        if producto.precio_venta<producto.precio_compra:
            flash("El precio de venta no puede ser menos al de compra", "warning")
            return redirect(request.url)

        imagen_file=request.files.get('imagen')

        if imagen_file and imagen_file.filename != '':
        
            if allowed_file(imagen_file.filename):
                if producto.imagen_public_id:
                    try:
                        cloudinary.uploader.destroy(producto.imagen_public_id)
                    except Exception as e:
                        print("Error eliminando imagen anterior:", e)
            
                resultado = cloudinary.uploader.upload(imagen_file,folder="productos")
                producto.imagen = resultado['secure_url']
                producto.imagen_public_id = resultado['public_id']
            else:
                flash("Formato de imagen no permitido", "danger")
                return redirect(request.url)
        
        db.session.commit()

        flash("Producto actualizado correctamente", "success")
        return redirect(url_for('routes_admin.panel'))
    
    categorias=Categoria.query.all()
    return render_template('admin/editar_producto.html', producto=producto, categorias=categorias)


@routes_admin.route('/pedidos')
@login_required
@admin_required
def ver_pedidos_admin():

    estado = request.args.get('estado')  # lee ?estado=...

    query = Pedido.query

    estados_validos = ['pendiente', 'pagado', 'entregado', 'cancelado']

    if estado and estado.lower() in estados_validos:
        query = query.filter(Pedido.estado.ilike(estado))

    pedidos = query.order_by(Pedido.fecha.desc()).all()

    if not pedidos:
        return render_template(
            'admin/ver_pedidos_admin.html',
            pedidos=[],
            mensaje="No hay pedidos con ese estado."
        )

    return render_template(
        'admin/ver_pedidos_admin.html',
        pedidos=pedidos,
        estado_actual=estado
    )

@routes_admin.route('/pedido/detalle/<int:pedido_id>')
@login_required
@admin_required
def detalle_pedido_admin(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)

    return render_template('admin/detalle_pedido_admin.html', pedido=pedido)


@routes_admin.route('/pedido/<int:pedido_id>/estado', methods=['POST'])
@login_required
@admin_required
def cambiar_estado_admin(pedido_id):
    pedido= Pedido.query.get_or_404(pedido_id)
    nuevo_estado = request.form.get("estado")

    ok, mensaje= cambiar_estado_pedido(pedido, nuevo_estado)

    if not ok:
        db.session.rollback()
        flash(mensaje, "error")
    else:
        db.session.commit()
        flash(mensaje, "success")
    
    return redirect(url_for('routes_admin.detalle_pedido_admin', pedido_id=pedido_id))


def reset_db():
    try:
        db.session.execute("SET FOREIGN_KEY_CHECKS=0")

        db.session.execute("TRUNCATE TABLE pedido_item")
        db.session.execute("TRUNCATE TABLE pedido")
        db.session.execute("TRUNCATE TABLE carrito_item")
        db.session.execute("TRUNCATE TABLE carrito")
        db.session.execute("TRUNCATE TABLE producto")

        db.session.execute("SET FOREIGN_KEY_CHECKS=1")
        db.session.commit()

        return "DB limpiada", 200

    except Exception as e:
        db.session.rollback()
        print(e)
        return "Error", 500