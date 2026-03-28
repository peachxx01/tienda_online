import re
from flask import Blueprint , session, request, render_template, redirect, url_for, flash
from models.db import db
from models.usuario import Usuario
from models.pedido import Pedido
from utils.decorators import login_required

routes_user= Blueprint('routes_user', __name__, url_prefix='/usuario')

def not_empty(*values):
    return all (v and str(v).strip() for v in values)

def is_valid_phone(phone):
    return bool(re.fullmatch(r"\d{7,15}", phone))

@routes_user.route('/panel')
@login_required
def panel():
    usuario = Usuario.query.get(session['user_id'])

    if not usuario:
        session.pop('user_id', None)
        flash("Por favor inicie sesión para acceder a esta página.", 'error')
        return redirect(url_for('routes_auth.login'))
    #Aunque tenga una validacion con el decorador, se encarga de no romper los templates si el usuario se elimina de imprevisto
    return render_template('usuarios/panel_usuario.html', usuario=usuario)


@routes_user.route('/perfil')
@login_required
def perfil():
    usuario = Usuario.query.get(session['user_id'])

    if not usuario:
        session.pop('user_id', None)
        flash("Por favor inicie sesión para acceder a esta página.", 'error')
        return redirect(url_for('routes_auth.login'))
    
    return render_template('usuarios/perfil.html', usuario=usuario)

@routes_user.route('/update', methods=['GET','POST'])
@login_required
def update_user():
    usuario = Usuario.query.get(session['user_id'])

    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('home'))

    if request.method == 'POST':

        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        direccion = request.form.get("direccion", "").strip()
        telefono = request.form.get("telefono", "").strip()
        
        if not not_empty(nombre, apellido):
            flash("Nombre y apellido son obligatorios", "error")
            return redirect(url_for('routes_user.perfil'))
        
        if telefono and not is_valid_phone(telefono):
            flash("Teléfono inválido (solo números de 7 a 15 digitos)", "error")
            return redirect(url_for('routes_user.perfil'))

        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.direccion = direccion
        usuario.telefono = telefono

        password_actual=request.form.get("password_actual")
        password_nueva=request.form.get("password_nueva")
        password_confirmacion= request.form.get("password_confirmacion")

        if password_actual or password_nueva or password_confirmacion:

            if not password_actual or not password_nueva or not password_confirmacion:
                flash("Para cambiar la contraseña complete todos los campos", "error")
                return redirect(url_for('routes_user.perfil'))
            
            if not usuario.verify_password(password_actual):
                flash("La contraseña actual es incorrecta", "error")
                return redirect(url_for('routes_user.perfil'))
            
            if password_nueva != password_confirmacion:
                flash("Las nuevas contraseñas no coinciden", "error")
                return redirect(url_for('routes_user.perfil'))
            
            usuario.hash_password(password_nueva)
            
        try:
            db.session.commit()
            flash("Perfil actualizado correctamente", "success")
        except Exception:
            db.session.rollback()
            flash("Error al actualizar el perfil", "error")
            return redirect(url_for('routes_user.perfil'))
    return render_template('usuarios/actualizar_usuario.html', usuario=usuario)

@routes_user.route('/pedidos')
@login_required
def ver_pedidos():
    usuario_id = session.get('user_id')

    pedidos = Pedido.query.filter_by(usuario_id=usuario_id).order_by(Pedido.fecha.desc()).all()
    if not pedidos:
        return render_template('usuarios/ver_pedidos_usuario.html', pedidos=[], mensaje="Aún no tienes pedidos.")

    return render_template('usuarios/ver_pedidos_usuario.html', pedidos=pedidos)


@routes_user.route('/pedido/detalle/<int:pedido_id>')
@login_required
def detalle_pedido(pedido_id):
    usuario_id = session.get('user_id')
    
    pedido = Pedido.query.filter_by(id_pedido=pedido_id, usuario_id=usuario_id).first()
    
    if not pedido:
        flash('El pedido no existe o no tienes permiso para verlo.', 'danger')
        return redirect(url_for('routes_user.ver_pedidos'))
    
    return render_template('usuarios/detalle_pedido_usuario.html', pedido=pedido)

