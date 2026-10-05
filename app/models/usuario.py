from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(100), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    ultimo_login = db.Column(db.DateTime, nullable=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    # --- MÉTODOS CRUD INICIAIS ---

    @classmethod
    def buscar_por_username(cls, username: str):
        """READ: Busca usuário ativo pelo nome de usuário."""
        return cls.query.filter_by(username=username, ativo=True).first()

    def verificar_senha(self, password: str) -> bool:
        """READ/Validação: Compara o hash gravado com a senha fornecida."""
        return check_password_hash(self.senha_hash, password)

    def registrar_acesso(self):
        """UPDATE: Atualiza a data e hora do último login realizado."""
        self.ultimo_login = datetime.now(timezone.utc)
        db.session.commit()

    @classmethod
    def criar_usuario(cls, username, nome, password):
        """CREATE: Função auxiliar para cadastrar usuários de teste com hash."""
        senha_criptografada = generate_password_hash(password)
        novo_usuario = cls(username=username, nome=nome, senha_hash=senha_criptografada)
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario