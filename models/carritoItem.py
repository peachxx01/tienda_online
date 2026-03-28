from models.db import db 

class CarritoItem(db.Model):
    __tablename__= 'carrito_item'
    id_carrito_item=db.Column(db.Integer, primary_key=True)
    carrito_id=db.Column(db.Integer, db.ForeignKey('carrito.id_carrito'))
    producto_id=db.Column(db.Integer, db.ForeignKey('producto.id_producto'))
    cantidad = db.Column(db.Integer, default=1)

    producto = db.relationship('Producto')

    def to_dict(self):
        return {
            'id': self.id_carrito_item,
            'producto_id': self.producto_id,
            'producto': self.producto.to_dict()
        }
