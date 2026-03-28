from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100), nullable=False)
    apellido=db.Column(db.String(100), nullable=False)
    email= db.Column(db.String(100), unique=True, nullable=False)
    password=db.Column(db.String(200), nullable=False)
    direccion=db.Column(db.String(200), nullable=True)
    rol= db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f"Usuario: {self.nombre}"
    
    def hash_password(self, password):
        self.password= generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre':self.nombre,
            'email': self.email,
            'rol': self.rol
        }