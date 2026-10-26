import sqlite3
import os

class DatabaseConnection:
    """
    Gerenciador de Conexão com o SQLite usando Context Manager.
    Garante o fechamento automático e o commit/rollback de transações.
    """
    def __init__(self, db_name: str = None):
        if db_name is None:
            db_name = os.environ.get('DB_NAME', 'perfil_viagens.db')
            
        app_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(app_dir, db_name)
        self.connection = None

    def __enter__(self):
        # Abre a conexão com o SQLite
        self.connection = sqlite3.connect(self.db_path)
        
        # 🔑 Configura o sqlite3.Row para permitir acessar colunas pelo nome (ex: row['username'])
        self.connection.row_factory = sqlite3.Row
        
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is not None:
                # Se ocorreu algum erro, desfaz as alterações (Rollback)
                self.connection.rollback()
            else:
                # Se deu tudo certo, salva as alterações (Commit)
                self.connection.commit()
            
            # Fecha a conexão com o banco
            self.connection.close()


def init_db(app=None):
    """
    Cria as tabelas iniciais no banco SQLite caso elas ainda não existam.
    Aceita 'app' opcionalmente para manter compatibilidade com o __init__.py.
    """
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                senha_hash TEXT NOT NULL,
                ultimo_login TEXT NULL,
                ativo INTEGER DEFAULT 1 NOT NULL
            );
        """)

        # ✈️ ATUALIZADA: Tabela de planos com colunas para pais e apartamento
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                continente TEXT NOT NULL,
                pais TEXT NOT NULL,
                apartamento TEXT NOT NULL,
                descricao TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            );
        """)