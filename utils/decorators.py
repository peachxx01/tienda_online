from functools import wraps
from flask import session, redirect, url_for, flash
from models.usuario import Usuario

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id=session.get('user_id')
        if not user_id:
            flash("Por favor inicie sesión para acceder a esta página.", 'error')
            return redirect(url_for('routes_auth.login'))
        usuario=Usuario.query.get(user_id)
        if not usuario:
            session.clear()
            flash("La sesión ya no es válida.", "error")
            return redirect(url_for('routes_auth.login'))

        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id=session.get('user_id')
        if not user_id:
            return redirect(url_for('routes_auth.login'))

        usuario=Usuario.query.get(user_id)

        if not usuario or usuario.rol.lower() != "admin":
            session.clear()
            flash("No tienes permisos para ingresar a esta página.", "error")
            return redirect(url_for('routes_auth.login'))

        return f(*args, **kwargs)
    return decorated_function
