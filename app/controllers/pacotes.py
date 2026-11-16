from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usuario import Usuario
from app.models.pacote import Pacote

pacote_bp = Blueprint('pacote', __name__)

@pacote_bp.route('/pacote/novo', methods=['GET', 'POST'])
def criar_pacote():
    username = session.get('usuario_logado')
    usuario = Usuario.buscar_por_username(username)

    if not usuario:
        session.clear()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        destino = request.form.get('destino')
        duracao_dias = request.form.get('duracao_dias')
        preco = request.form.get('preco')
        descricao = request.form.get('descricao')

        if not all([titulo, destino, duracao_dias, preco, descricao]):
            flash('Preencha todos os campos do pacote!', 'danger')
            return render_template('criar_pacote.html')

        novo_pacote = Pacote(
            usuario_id=usuario.id,
            titulo=titulo,
            destino=destino,
            duracao_dias=int(duracao_dias),
            preco=float(preco),
            descricao=descricao
        )
        novo_pacote.salvar()

        flash('Pacote de viagem publicado com sucesso!', 'success')
        return redirect(url_for('plano.dashboard'))

    return render_template('criar_pacote.html')