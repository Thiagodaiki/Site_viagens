from flask import session, redirect, url_for, request

# Libera o registro para acesso público
ROTAS_PUBLICAS = ['auth.login', 'auth.register', 'auth.index', 'static']

def verificar_autenticacao():
    endpoint = request.endpoint

    if endpoint and endpoint not in ROTAS_PUBLICAS:
        if 'usuario_logado' not in session:
            return redirect(url_for('auth.login'))