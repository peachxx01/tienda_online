from models.db import db

class PedidoItem(db.Model):
    __tablename__= 'pedido_item'
    id_pedido_item=db.Column(db.Integer, primary_key=True)
    pedido_id=db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), nullable=False)
    producto_id=db.Column(db.Integer, db.ForeignKey('producto.id_producto', ondelete='RESTRICT'), nullable=False)
    cantidad=db.Column(db.Integer, nullable=False)
    precio_unitario= db.Column(db.Float, nullable=False)
    costo_unitario= db.Column(db.Float, nullable=False)
    subtotal=db.Column(db.Float, nullable=False)

    producto = db.relationship("Producto")

    def __repr__(self):
        return f"Pedido Item Pedido:{self.pedido_id}, Producto: {self.producto_id}"