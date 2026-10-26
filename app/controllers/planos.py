from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usuario import Usuario
from app.models.plano import Plano

# Cria o Blueprint separado para os planos
plano_bp = Blueprint('plano', __name__)

@plano_bp.route('/plano/novo', methods=['GET', 'POST'])
def criar_plano():
    username = session.get('usuario_logado')
    usuario = Usuario.buscar_por_username(username)

    if not usuario:
        session.clear()
        flash('Sessão inválida. Faça login novamente.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        continente = request.form.get('continente')
        pais = request.form.get('pais')
        apartamento = request.form.get('apartamento')
        descricao = request.form.get('descricao')

        if not continente or not pais or not apartamento or not descricao:
            flash('Preencha todos os campos!', 'danger')
            return render_template('criar_plano.html')

        novo_plano = Plano(
            usuario_id=usuario.id,
            continente=continente,
            pais=pais,
            apartamento=apartamento,
            descricao=descricao
        )
        novo_plano.salvar()

        flash('Plano de viagem criado com sucesso!', 'success')
        return redirect(url_for('auth.dashboard'))

    return render_template('criar_plano.html')