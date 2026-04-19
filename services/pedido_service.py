from models.db import db

TRANSICIONES_VALIDAS={
    "pendiente": ["pagado", "cancelado"],
    "pagado":["entregado", "cancelado"],
    "entregado":[],
    "cancelado":[]
}

#CAMBIO DE ESTADO DE PEDIDOS
def cambiar_estado_pedido(pedido, nuevo_estado):

    if nuevo_estado not in TRANSICIONES_VALIDAS.get(pedido.estado, []):
        return False, "Transición inválida"
    
    if pedido.estado=="pendiente" and nuevo_estado=="pagado":
        for item in pedido.items:
            producto=item.producto

            if not producto.activo:
                return False, f"El producto '{producto.nombre}' ya no está disponible"

            if producto.stock < item.cantidad:
                return False, f"Stock insuficiente para {producto.nombre}"
            
        for item in pedido.items:
            producto=item.producto
            producto.stock -= item.cantidad
    
    if pedido.estado == "pagado" and nuevo_estado=="cancelado":
        for item in pedido.items:
            producto= item.producto
            producto.stock += item.cantidad

    pedido.estado=nuevo_estado

    return True, "Estado actualizado correctamente"

            