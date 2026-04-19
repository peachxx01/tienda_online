from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from models.db import db
from models.usuario import Usuario

routes_auth=Blueprint('routes_auth', __name__, url_prefix='/auth' )


#REGISTRO
@routes_auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        nombre=request.form['nombre']
        apellido=request.form['apellido']
        email=request.form['email']
        password=request.form['password']

        existing_user=Usuario.query.filter(Usuario.email==email).first()
        if existing_user:
            flash("Email ya registrado, pruebe con otro.", "error")
            return redirect(url_for('routes_auth.register'))
        
        nuevo_usuario= Usuario(nombre=nombre, apellido=apellido, email=email, rol="cliente")
        nuevo_usuario.hash_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Se ha creado el usuario correctamente", "success")
        return redirect (url_for('routes_auth.login'))
    return render_template('usuarios/register.html')


#LOGIN
@routes_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        if not email or not password:
            flash("Los campos son obligatorios", "warning")
            return redirect(url_for('routes_auth.login'))
        else:
            usuario=Usuario.query.filter(Usuario.email==email).first()
            if usuario and usuario.verify_password(password):
                session['user_id']= usuario.id
                session['user_nombre']=usuario.nombre
                session['user_rol']= usuario.rol
                flash(f"Bienvenido/a, {usuario.nombre}", "success")
                return redirect(url_for('home'))
            else:
                flash("Email o contraseña incorrectos.", "error")
                return redirect(url_for('routes_auth.login'))
    return render_template('usuarios/login.html')


#LOGOUT
@routes_auth.route('/logout', methods=['POST'])
def logout():
    if request.method=='POST':
        flash("Sesión cerrada.", "success")
        session.clear()
        return redirect(url_for('home'))