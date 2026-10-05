from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
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

        # READ no SQL Server via ORM
        usuario = Usuario.buscar_por_username(username)

        if usuario and usuario.verificar_senha(password):
            # UPDATE no SQL Server (Registra a data do acesso)
            usuario.registrar_acesso()

            # Sessão do Flask
            session['usuario_logado'] = usuario.username
            session['nome_usuario'] = usuario.nome
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'usuario_logado' in session:
        return redirect(url_for('auth.dashboard'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 1. Validação de senha
        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return render_template('register.html')

        # 2. Verifica se o usuário já existe no SQLite
        usuario_existente = Usuario.buscar_por_username(username)
        if usuario_existente:
            flash('Nome de usuário já cadastrado. Escolha outro.', 'danger')
            return render_template('register.html')

        # 3. Cria o usuário e grava no banco
        Usuario.criar_usuario(username=username, nome=nome, password=password)
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

    
@auth_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', nome=session.get('nome_usuario'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))