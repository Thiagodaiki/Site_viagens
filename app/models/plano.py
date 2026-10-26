from app.database import DatabaseConnection

class Plano:
    def __init__(self, usuario_id: int, continente: str, pais: str, apartamento: str, descricao: str, id: int = None):
        self.id = id
        self.usuario_id = usuario_id
        self.continente = continente
        self.pais = pais
        self.apartamento = apartamento
        self.descricao = descricao

    @classmethod
    def _instanciar_da_row(cls, row):
        """Converte uma sqlite3.Row em uma instância de Plano."""
        if not row:
            return None
        return cls(
            id=row['id'],
            usuario_id=row['usuario_id'],
            continente=row['continente'],
            pais=row['pais'],
            apartamento=row['apartamento'],
            descricao=row['descricao']
        )

    @classmethod
    def buscar_por_usuario(cls, usuario_id: int):
        """Retorna todos os planos de um usuário específico."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM planos WHERE usuario_id = ?", (usuario_id,))
            rows = cursor.fetchall()
            return [cls._instanciar_da_row(row) for row in rows]

    def salvar(self):
        """Insere um novo plano no banco de dados."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO planos (usuario_id, continente, pais, apartamento, descricao)
                VALUES (?, ?, ?, ?, ?)
            """, (self.usuario_id, self.continente, self.pais, self.apartamento, self.descricao))
            self.id = cursor.lastrowid