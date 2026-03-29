from flask import Flask, render_template, flash, request, redirect
import os

# Importamos tu configuración
import config.config as config

app = Flask(__name__)

# Cargamos la configuración (asegurate que los nombres en config.py coincidan con Railway)
app.config.from_object(config)

# --- RUTAS DE PRUEBA (Para matar el 502) ---

@app.route('/')
def home_test():
    return "<h1>¡Servidor Funcionando!</h1><p>Si ves esto, el 502 ha muerto. Ahora podemos empezar a descomentar el resto.</p>", 200

@app.route('/health')
def health():
    return "App viva", 200

# --- EL RESTO DEL CÓDIGO (COMENTADO PARA DIAGNÓSTICO) ---
"""
# Cuando funcione el /health, empezaremos a descomentar esto:
from models.db import db
from models.categoria import Categoria
from routes.routes_categorias import routes_categorias
# ... (demás imports)

db.init_app(app)

@app.context_processor
def inject_categorias():
    if request.endpoint == 'static':
        return {}
    return {'categorias': Categoria.query.all()}

app.register_blueprint(routes_categorias)
# ... (demás registros)
"""

if __name__ == '__main__':
    # Forzamos el puerto 8080 que configuramos en Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)