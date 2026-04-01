from models.db import db 

#En este modelo uso index para que cuando se use la funcion de buscar producto no sea lenta la lectura en BD

class Producto(db.Model):
    __tablename__ = 'producto'
    id_producto= db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(100), index=True , nullable=False)
    precio_venta= db.Column(db.Float, nullable=False)
    precio_compra= db.Column(db.Float, nullable=False)
    activo = db.Column(db.Boolean, default=True, index=True)
    descripcion = db.Column(db.Text, nullable=True)
    stock= db.Column(db.Integer, nullable=False)
    imagen= db.Column(db.String(200), nullable=True)
    imagen_public_id = db.Column(db.String(200), nullable=True)
    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey('categoria.id_categoria'),
        index=True,
        nullable=False
    )
    categoria = db.relationship('Categoria')
    popular = db.Column(db.Boolean, index=True, default=False) 
    
    def to_dict(self):
        return {
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'precio_venta': self.precio_venta,
            'precio_compra': self.precio_compra,
            'activo': self.activo,
            'descripcion': self.descripcion,
            'stock': self.stock,
            'imagen': self.imagen,
            'categoria': {
                'id': self.categoria.id_categoria,
                'nombre': self.categoria.nombre},
            'popular': self.popular
        }