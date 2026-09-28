from werkzeug.security import generate_password_hash, check_password_hash

# Simulação do banco de dados na memória
# As senhas são gravadas como hashes seguros
USUARIOS_DB = {
    "viajante1": {
        "nome": "Carlos Silva",
        "senha_hash": generate_password_hash("senha123")
    },
    "maria_viagens": {
        "nome": "Maria Oliveira",
        "senha_hash": generate_password_hash("viagem2026")
    }
}

class UserModel:
    @staticmethod
    def autenticar(username, password):
        """Valida se o usuário existe e se a senha está correta."""
        usuario = USUARIOS_DB.get(username)
        if usuario and check_password_hash(usuario["senha_hash"], password):
            return {"username": username, "nome": usuario["nome"]}
        return None

