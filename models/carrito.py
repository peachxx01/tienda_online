from models.db import db

class Carrito(db.Model):
    __tablename__ = 'carrito'
    id_carrito= db.Column(db.Integer, primary_key=True)
    usuario_id= db.Column(db.Integer, db.ForeignKey('usuario.id'))
    estado= db.Column(db.String(20), default='activo')

    items = db.relationship(
    'CarritoItem',
    backref='carrito',
    lazy=True
    )

    def to_dict(self):
        return {
            'id': self.id_carrito,
            'estado': self.estado,
            'items': [item.to_dict() for item in self.items]
        }


    