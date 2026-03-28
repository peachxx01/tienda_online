from datetime import datetime
from models.db import db

class Pedido(db.Model):
    __tablename__='pedido'
    id_pedido=db.Column(db.Integer, primary_key=True)
    usuario_id= db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    fecha=db.Column(db.DateTime, default=datetime.utcnow)
    total=db.Column(db.Float, nullable=False, default=0)
    estado=db.Column(db.String(20), default='pendiente', nullable=False)

    usuario = db.relationship('Usuario', backref='pedidos', lazy=True)

    items=db.relationship('PedidoItem', backref='pedido', lazy=True, cascade='all, delete-orphan')
    #Se usa cascade para que si se borra un pedido, se borran los items
    def __repr__(self):
        return f"Pedido {self.id_pedido}- Usuario {self.usuario_id}"
    