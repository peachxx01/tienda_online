from flask import Flask
import os
import config.config as config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def simple_home():
    return "Hola! Si ves esto, el servidor funciona.", 200

@app.route('/health')
def health():
    return "App viva", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)