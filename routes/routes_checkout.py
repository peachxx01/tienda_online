from flask import Blueprint, session, flash, redirect, request, url_for, current_app
from utils.decorators import login_required
from models.db import db
from models.pedido import Pedido
from models.pedidoItem import PedidoItem
from services.payment_service import crear_preferencia
from services.pedido_service import cambiar_estado_pedido
from routes.routes_carrito import obtener_carrito_activo 
import mercadopago


routes_checkout=Blueprint('routes_checkout', __name__, url_prefix='/checkout')

#CHECKOUT(SE BORRA EL CARRITO, SE CREA PEDIDO Y SE HACE EL INIT POINT)
@routes_checkout.route('/', methods=['POST'])
@login_required
def checkout():
    try:
        usuario_id= session.get("user_id")
        carrito=obtener_carrito_activo(usuario_id)

        if not carrito or not carrito.items:
            flash("El carrito esta vacío.", "error")
            return redirect(url_for('routes_carrito.ver_carrito'))

        for item in carrito.items:
            if not item.producto.activo:
                flash(f"El producto '{item.producto.nombre}' ya no está disponible.", "error")
                return redirect(url_for('routes_carrito.ver_carrito'))
    
        for item in carrito.items:
            if item.cantidad>item.producto.stock:
                flash("No hay suficiente stock.", "error")
                return redirect(url_for('routes_carrito.ver_carrito'))
        
        total=sum(item.producto.precio_venta*item.cantidad for item in carrito.items)

        pedido=Pedido.query.filter_by(usuario_id=usuario_id, estado="pendiente").first()

        if not pedido:
            pedido=Pedido(usuario_id=usuario_id,total=total, estado="pendiente")
            db.session.add(pedido)
            db.session.flush()#commit temporal para poder usar pedido_id
        else:
            pedido.total=total
            PedidoItem.query.filter_by(pedido_id=pedido.id_pedido).delete()

        for item in carrito.items:
            subtotal_item = item.producto.precio_venta * item.cantidad
            
            pedido_item=PedidoItem(
                pedido_id=pedido.id_pedido,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio_venta,
                costo_unitario=item.producto.precio_compra,
                subtotal=subtotal_item
            )
            db.session.add(pedido_item)

        init_point = crear_preferencia(pedido)

        db.session.commit()

        return redirect(init_point)
    except Exception as e:
        db.session.rollback()
        print(e)
        flash("Ocurrió un error al procesar la compra", "error")
        return redirect(url_for('routes_carrito.ver_carrito'))


#MERCADO PAGO VUELVE A ESTA RUTA SI HUBO EXITO
@routes_checkout.route('/success')
@login_required
def pago_success():
    flash("Estamos procesando tu pago, revisa el apartado de Mis  Pedidos", "info")
    return redirect(url_for('home'))

#MERCADO PAGO VUELVE A ESTA RUTA SI HAY UN FALLO
@routes_checkout.route('/failure')
@login_required
def pago_failure():
    flash("El pago fue rechazado. Intentá nuevamente", "error")
    return redirect(url_for('routes_carrito.ver_carrito'))

#MERCADO PAGO VUELVE A ESTA RUTA SI LA CONEXION QUEDO PENDIENTE
@routes_checkout.route('/pending')
@login_required
def pago_pending():
    flash("Tu pago está pendiente de confirmación", "warning")
    return redirect(url_for('home'))


#NOTIFICACION DE PAGO POR PARTE DE MERCADO PAGO
@routes_checkout.route('/webhook', methods=['POST'])
def webhook_mp():
    try:
        data=request.json 
        print("webhook recibido: ", data)

        if not data:
            return "No data", 400

        tipo = data.get("type") or data.get("topic")

        if tipo != "payment":#procesa solamente pagos
            print("Evento ignorado:", tipo)
            return "OK", 200

        payment_id= data.get("data", {}).get("id")

        if not payment_id:
            return "No payment id", 400

        sdk=mercadopago.SDK(current_app.config['MP_ACCESS_TOKEN'])

        payment_response=sdk.payment().get(payment_id)

        if payment_response["status"]!=200:
            return "error al consultar pago", 400
        
        payment_info=payment_response["response"]

        status=payment_info.get("status")

        external_reference=payment_info.get("external_reference")

        print("status:", status)
        print("pedido id:", external_reference)

        if not external_reference:
            return "no external reference", 400

        pedido= Pedido.query.get(external_reference)

        if not pedido:
            return "Pedido no encontrado", 400
        
        if pedido.estado == "pagado": #EVITAR PAGOS DUPLICADOS
            return "OK", 200

        if status == "approved":
            ok, mensaje = cambiar_estado_pedido(pedido, "pagado")

            if not ok:
                db.session.rollback()
                return mensaje, 400

            carrito = obtener_carrito_activo(pedido.usuario_id)

            if carrito:
                carrito.estado = "inactivo"
        elif status in ["rejected", "cancelled"]:
            ok, mensaje = cambiar_estado_pedido(pedido, "cancelado")

            if not ok:
                db.session.rollback()
                return mensaje, 400
        else:
            print("Estado ignorado:", status)
            return "OK", 200
        
        db.session.commit()
        return "OK", 200
    except Exception as e:
        db.session.rollback()
        print("Error en webhook: ", e)
        return "Error", 500


