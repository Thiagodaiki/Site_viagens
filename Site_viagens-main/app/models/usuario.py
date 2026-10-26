from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import DatabaseConnection

class Usuario:
    def __init__(self, username: str, nome: str, senha_hash: str, id: int = None, ultimo_login: str = None, ativo: bool = True):
        self.id = id
        self.username = username
        self.nome = nome
        self.senha_hash = senha_hash
        self.ultimo_login = ultimo_login
        self.ativo = ativo

    # =========================================================================
    # MÉTODOS DE CLASSE (Consultas / Buscas / Criadores)
    # =========================================================================

    @classmethod
    def _instanciar_da_row(cls, row):
        """Converte uma sqlite3.Row em uma instância da classe Usuario."""
        if not row:
            return None
        
        # 🔑 Acesso direto pelo nome da coluna graças ao sqlite3.Row
        return cls(
            id=row['id'],
            username=row['username'],
            nome=row['nome'],
            senha_hash=row['senha_hash'],
            ultimo_login=row['ultimo_login'],
            ativo=bool(row['ativo'])
        )

    @classmethod
    def buscar_por_username(cls, username: str):
        """Busca um usuário ativo no banco pelo username."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM usuarios WHERE username = ? AND ativo = 1", 
                (username,)
            )
            row = cursor.fetchone()
            return cls._instanciar_da_row(row)
        
 

    @classmethod
    def buscar_por_id(cls, user_id: int):
        """Busca um usuário no banco pelo ID."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return cls._instanciar_da_row(row)

    @classmethod
    def criar_usuario(cls, username: str, nome: str, password: str):
        """Cria um novo usuário criptografando a senha e salva no banco."""
        senha_criptografada = generate_password_hash(password)
        novo_usuario = cls(username=username, nome=nome, senha_hash=senha_criptografada)
        novo_usuario.salvar()
        return novo_usuario

    # =========================================================================
    # MÉTODOS DE INSTÂNCIA (Comportamentos e Persistência do Objeto)
    # =========================================================================

    def salvar(self):
        """Persiste o objeto no banco de dados (CREATE ou UPDATE)."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            
            if self.id is None:
                # INSERT (Novo usuário)
                cursor.execute("""
                    INSERT INTO usuarios (username, nome, senha_hash, ultimo_login, ativo)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.username, self.nome, self.senha_hash, self.ultimo_login, int(self.ativo)))
                
                # Atribui o ID gerado automaticamente pelo banco ao próprio objeto
                self.id = cursor.lastrowid
            else:
                # UPDATE (Usuário existente)
                cursor.execute("""
                    UPDATE usuarios 
                    SET username = ?, nome = ?, senha_hash = ?, ultimo_login = ?, ativo = ?
                    WHERE id = ?
                """, (self.username, self.nome, self.senha_hash, self.ultimo_login, int(self.ativo), self.id))

    def verificar_senha(self, password: str) -> bool:
        """Valida se a senha informada corresponde ao hash gravado."""
        return check_password_hash(self.senha_hash, password)

    def registrar_acesso(self):
        """Atualiza o atributo ultimo_login do objeto e persiste no banco."""
        self.ultimo_login = datetime.now(timezone.utc).isoformat()
        self.salvar() # Executa o UPDATE via Active Record

    def desativar(self):
        """Desativa a conta do usuário (Soft Delete)."""
        self.ativo = False
        self.salvar()