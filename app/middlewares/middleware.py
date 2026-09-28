from flask import session, redirect, url_for, request

# Rotas que NÃO precisam de autenticação
ROTAS_PUBLICAS = ['auth.login', 'static']

def verificar_autenticacao():
    """Middleware executado antes de cada requisição."""
    endpoint = request.endpoint

    # Se a rota existe e não é pública, verifica se o usuário está logado
    if endpoint and endpoint not in ROTAS_PUBLICAS:
        if 'usuario_logado' not in session:
            return redirect(url_for('auth.login'))