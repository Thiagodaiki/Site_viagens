import os
from flask import Flask
from app.middlewares.middleware import verificar_autenticacao
from app.controllers.auth import auth_bp

def create_app():
    # Define o caminho correto para a pasta 'view' como pasta de templates
    app_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(app_dir, 'views', 'templates')
    static_dir = os.path.join(app_dir, 'views', 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Chave secreta obrigatória para assinar e proteger os cookies de sessão
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave_secreta_para_desenvolvimento')

    # Registra o middleware global antes de cada requisição
    app.before_request(verificar_autenticacao)

    # Registra o Blueprint
    app.register_blueprint(auth_bp)

    return app