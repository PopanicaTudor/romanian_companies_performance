from flask import Flask
from app.routes import main

def create_app():
    """
    Creează și configurează aplicația Flask.
    """
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SECRET_KEY'] = 'cheie-secreta-de-schimbat'

    # Înregistrăm blueprint-ul pentru rute
    app.register_blueprint(main)

    return app