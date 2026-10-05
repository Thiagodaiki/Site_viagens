import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Configura e inicializa a conexão com o SQLite."""
    
    app_dir = os.path.dirname(os.path.abspath(__file__))
    dbname = os.environ.get('DB_NAME', 'perfil_viagens.db')
    
    # Caminho onde o arquivo .db será criado (dentro da pasta app)
    db_path = os.path.join(app_dir, dbname)
    
    # URL de conexão do SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)