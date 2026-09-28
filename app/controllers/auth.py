from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usuario import UserModel

# Criação do Blueprint com a pasta de views customizada
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Redireciona a raiz ('/') para a página correta."""
    if 'usuario_logado' in session:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_logado' in session:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usuario = UserModel.autenticar(username, password)

        if usuario:
            # Armazena dados do usuário na sessão criptografada
            session['usuario_logado'] = usuario['username']
            session['nome_usuario'] = usuario['nome']
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', nome=session.get('nome_usuario'))

@auth_bp.route('/logout')
def logout():
    session.clear()  # Limpa a sessão
    return redirect(url_for('auth.login'))