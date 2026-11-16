from app.database import DatabaseConnection

class Pacote:
    def __init__(self, usuario_id: int, titulo: str, destino: str, duracao_dias: int, preco: float, descricao: str, id: int = None, autor_nome: str = None):
        self.id = id
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.destino = destino
        self.duracao_dias = duracao_dias
        self.preco = preco
        self.descricao = descricao
        self.autor_nome = autor_nome  # Campo extra preenchido via JOIN na listagem pública

    @classmethod
    def _instanciar_da_row(cls, row):
        if not row:
            return None
        return cls(
            id=row['id'],
            usuario_id=row['usuario_id'],
            titulo=row['titulo'],
            destino=row['destino'],
            duracao_dias=row['duracao_dias'],
            preco=row['preco'],
            descricao=row['descricao'],
            autor_nome=row['autor_nome'] if 'autor_nome' in row.keys() else None
        )

    @classmethod
    def listar_todos_publicos(cls):
        """Busca todos os pacotes cadastrados por qualquer usuário, trazendo o nome do criador."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pacotes.*, usuarios.nome AS autor_nome
                FROM pacotes
                INNER JOIN usuarios ON pacotes.usuario_id = usuarios.id
                ORDER BY pacotes.id DESC
            """)
            rows = cursor.fetchall()
            return [cls._instanciar_da_row(row) for row in rows]

    def salvar(self):
        """Salva um novo pacote no banco de dados."""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pacotes (usuario_id, titulo, destino, duracao_dias, preco, descricao)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.usuario_id, self.titulo, self.destino, self.duracao_dias, self.preco, self.descricao))
            self.id = cursor.lastrowid