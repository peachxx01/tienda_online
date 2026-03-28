from models.db import db
#En este modelo uso index para que cuando se use la funcion de buscar producto no sea lenta la lectura en BD

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), index=True, nullable=False)
    slug = db.Column(db.String(50), index=True, nullable=False, unique=True)
    
    productos = db.relationship('Producto', back_populates='categoria')


