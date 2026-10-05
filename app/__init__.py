import os
from flask import Flask
from dotenv import load_dotenv
from app.database import db, init_db
from app.middlewares.middleware import verificar_autenticacao
from app.controllers.auth import auth_bp

load_dotenv()

def create_app():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(app_dir, 'views', 'templates')
    static_dir = os.path.join(app_dir, 'views', 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave_dev_fallback')

    # Inicializa o SQLite
    init_db(app)

    # Importa o modelo para que o SQLAlchemy reconheça as tabelas
    from app.models.usuario import Usuario

    with app.app_context():
        # Cria o arquivo perfil_viagens.db e a tabela 'usuarios' se não existirem
        db.create_all()

        # Cria um usuário de teste inicial se o banco estiver vazio
        if not Usuario.buscar_por_username('viajante1'):
            Usuario.criar_usuario(
                username='viajante1',
                nome='Carlos Silva',
                password='senha123'
            )

    app.before_request(verificar_autenticacao)
    app.register_blueprint(auth_bp)

    return app