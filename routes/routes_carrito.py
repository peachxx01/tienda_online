from flask import Blueprint, redirect, render_template, url_for, flash, request, session, abort
from models.carrito import Carrito
from models.carritoItem import CarritoItem
from models.producto import Producto
from models.db import db
from utils.decorators import login_required

routes_carrito= Blueprint('routes_carrito', __name__, url_prefix='/carrito')

def obtener_carrito_activo(usuario_id):
    carrito=Carrito.query.filter_by(usuario_id=usuario_id, estado="activo").first()

    if not carrito:
        carrito=Carrito(usuario_id=usuario_id, estado="activo")
        db.session.add(carrito)
        db.session.commit()
    return carrito

@routes_carrito.route("/ver")
@login_required
def ver_carrito():
    usuario_id=session.get('user_id')
    
    carrito=Carrito.query.filter_by(usuario_id=usuario_id, estado="activo").first()

    if not carrito:
        return render_template("carrito/carrito.html", items=[], total=0)
    
    total=sum(item.producto.precio_venta * item.cantidad 
              for item in carrito.items)
    
    return render_template("carrito/carrito.html", items=carrito.items, total=total)

@routes_carrito.route("/agregar/<int:id_producto>", methods=['POST'])
@login_required
def agregar_al_carrito(id_producto):
    usuario_id=session.get('user_id')
    
    producto = Producto.query.filter_by(id_producto=id_producto,activo=True).first_or_404()

    if producto.stock<=0:
        flash("Producto sin stock", "error")
        return redirect(request.referrer)
    
    carrito=obtener_carrito_activo(usuario_id)

    item=CarritoItem.query.filter_by(carrito_id=carrito.id_carrito, producto_id=id_producto).first()

    if item:
        if item.cantidad>=producto.stock:
            flash("No hay stock disponible en este momento.", "error")
            return redirect(request.referrer)
        item.cantidad +=1
    else:
        nuevo_item=CarritoItem(carrito_id=carrito.id_carrito, producto_id=id_producto, cantidad=1)
        db.session.add(nuevo_item)
    
    db.session.commit()

    flash("Producto agregado al carrito", "success")
    return redirect(request.referrer)

@routes_carrito.route('/aumentar/<int:id_item>', methods=['POST'])
@login_required
def aumentar_cantidad(id_item):
    usuario_id=session.get('user_id')
    
    item=CarritoItem.query.get_or_404(id_item)

    if item.carrito.usuario_id !=usuario_id:
        abort(403)

    if item.cantidad >= item.producto.stock:
        flash("Stock máximo alcanzado", "error")
        return redirect(url_for('routes_carrito.ver_carrito'))
    
    item.cantidad +=1
    db.session.commit()

    return redirect(url_for('routes_carrito.ver_carrito'))

@routes_carrito.route('/disminuir/<int:id_item>', methods=['POST'])
@login_required
def disminuir_cantidad(id_item):
    usuario_id =session.get('user_id')

    item= CarritoItem.query.get_or_404(id_item)

    if item.carrito.usuario_id !=usuario_id:
        abort(403)

    if item.cantidad <=1:
        db.session.delete(item)
    else:
        item.cantidad -=1
    
    db.session.commit()

    return redirect(url_for('routes_carrito.ver_carrito'))


@routes_carrito.route('/eliminar/<int:id_item>', methods=['POST'])
@login_required
def eliminar_item(id_item):
    usuario_id =session.get('user_id')
    
    item=CarritoItem.query.get_or_404(id_item)

    if item.carrito.usuario_id != usuario_id:
        abort(403)

    db.session.delete(item)
    db.session.commit()

    flash("Producto eliminado de carrito", "success")
    return redirect(url_for('routes_carrito.ver_carrito'))