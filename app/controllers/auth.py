from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Redireciona para o dashboard se logado, ou para a tela de login."""
    if 'usuario_logado' in session:
        return redirect(url_for('plano.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Exibe e processa a autenticação do usuário."""
    if 'usuario_logado' in session:
        return redirect(url_for('plano.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usuario = Usuario.buscar_por_username(username)

        if usuario and usuario.verificar_senha(password):
            usuario.registrar_acesso()
            session['usuario_logado'] = usuario.username
            session['nome_usuario'] = usuario.nome
            
            return redirect(url_for('plano.dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Exibe e processa o cadastro de novos usuários."""
    if 'usuario_logado' in session:
        return redirect(url_for('plano.dashboard'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return render_template('register.html')

        if Usuario.buscar_por_username(username):
            flash('Nome de usuário já cadastrado. Escolha outro.', 'danger')
            return render_template('register.html')

        Usuario.criar_usuario(username=username, nome=nome, password=password)

        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    """Encerra a sessão do usuário."""
    session.clear()
    return redirect(url_for('auth.login'))