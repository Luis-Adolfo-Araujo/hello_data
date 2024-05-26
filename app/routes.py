from utils import *
import psycopg2
from flask import request, jsonify, render_template, flash, Blueprint, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from .models import Paciente

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

@auth.route("/", methods=["GET"])
def main_route():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    return render_template("public/index.html")

@auth.route("/home", methods=["GET"])
@login_required
def home():
    try:
        if current_user.is_authenticated:
            return render_template("public/templates/home.html")
    except:
        return redirect(url_for('auth.main_route'))

@auth.route("/login")
def render_login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    return render_template("public/templates/login.html")

@auth.route("/login_post", methods=["POST"])
def login():
    email = request.form['email']
    senha = request.form['senha']
    conn, cursor = get_db_connection()

    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        query = '''SELECT * FROM paciente WHERE email = %s;'''
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()
        print("user: ", user_data)
        if user_data is None or not check_password_hash(user_data['senha'], senha):
            error = "Email ou senha incorretos"
            flash(error, 'login_error')
            return redirect(url_for('auth.render_login'))

        user_id = user_data['user_id']
        user = Paciente(user_id=user_id)
        login_user(user)
        return redirect(url_for('auth.home'))
    except psycopg2.Error as e:
        print("Error during query execution:", e)
        return jsonify({"error": "Error during query execution"}), 500
    finally:
        cursor.close()
        conn.close()


@auth.route("/signup")
def signup():
    return render_template('public/templates/signup.html')

@auth.route("/register", methods=["POST"])
def signup_post():
    conn, cursor = get_db_connection()
    
    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        sexo = request.form.get('sexo')
        gestante = True if sexo == 'feminino' and request.form.get('gestante') == 'sim' else False
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        cep = request.form.get('cep')
        rua = request.form.get('rua')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        uf = request.form.get('uf')
        query = '''SELECT cpf FROM paciente WHERE cpf = %s;'''
        cursor.execute(query, (cpf,))
        user = cursor.fetchone()

        if user:
            error_message = "CPF ja cadastrado"
            redirect(url_for('auth.signup'))
            print(error_message)
            return jsonify({"error": error_message}), 400
        
        insert_query = '''INSERT INTO paciente (email, senha, nome, data_nascimento, sexo, gestante, telefone, cpf, cep, rua, numero, bairro, cidade, uf)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        cursor.execute(insert_query, (email, generate_password_hash(senha), nome, data_nascimento, sexo, gestante, telefone, cpf, cep, rua, numero, bairro, cidade, uf))
        conn.commit()

        print("Usuário cadastrado com sucesso!")
        return redirect(url_for('auth.render_login'))

    except Exception as e:
        print("Erro ao cadastrar usuário: " + str(e))
        return redirect(url_for('auth.signup'))
    
    finally:
        cursor.close()
        conn.close()
    

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("public/index.html")

@auth.route("/anamnese_post", methods=["POST"])
@login_required
def anamnese_post():
    conn, cursor = get_db_connection()
    
    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    try:
        id_usuario = current_user.id

        objetivo = request.form.get('objetivo')
        restricao_alimentar = request.form.get('restricao_alimentar')
        ingere_alcool = request.form.get('ingere_alcool')
        dorme_bem = True if request.form.get('dorme_bem') == 'sim' else False
        horas_sono = request.form.get('horas_sono')
        pratica_exercicios = True if request.form.get('pratica_exercicios') == 'sim' else False
        patologia = request.form.get('patologia')
        medicamentos = request.form.get('medicamentos')
        apetite = request.form.get('apetite')
        mastigacao = request.form.get('mastigacao')
        habito_intestinal = request.form.get('habito_intestinal')
        frequencia_evacuacao = request.form.get('frequencia_evacuacao')
        formato_fezes = request.form.get('formato_fezes')
        usa_laxante = True if request.form.get('usa_laxante') == 'sim' else False
        cor_fezes = request.form.get('cor_fezes')
        ingestao_hidrica = request.form.get('ingestao_hidrica')
        sintomas = request.form.get('sintomas')

        insert_query = '''
            INSERT INTO info_paciente (
                id_usuario, objetivo, resticao_alimentar, ingere_alcool, dorme_bem, horas_sono, 
                pratica_exercicios, patologia, Medicamentos, apetite, mastigacao, habito_intestinal, 
                frequencia_evacuacao, formato_fezes, usa_laxante, cor_fezes, ingestao_hidrica, sintomas
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

        cursor.execute(insert_query, (
            id_usuario, objetivo, restricao_alimentar, ingere_alcool, dorme_bem, horas_sono, 
            pratica_exercicios, patologia, medicamentos, apetite, mastigacao, habito_intestinal, 
            frequencia_evacuacao, formato_fezes, usa_laxante, cor_fezes, ingestao_hidrica, sintomas
        ))

        conn.commit()
        flash('Informações de anamnese salvas com sucesso!', 'success')
        return redirect(url_for('auth.metabolic'))

    except Exception as e:
        conn.rollback()
        print("Erro ao salvar informações de anamnese: " + str(e))
        return redirect(url_for('auth.anamnese'))

    finally:
        cursor.close()
        conn.close()


@auth.route("/anamnese")
@login_required
def anamnese():
    return render_template("public/templates/anamnesis.html")

@auth.route("/metabolic")
@login_required
def metabolic():
    return render_template("public/templates/metabolic.html")

@auth.route("/metabolic_post", methods=["POST"])
@login_required
def metabolic_post():
    conn, cursor = get_db_connection()
    
    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        id_usuario = current_user.id
        tontura = request.form.get('tontura') == 'sim'
        sensacao_desmaio = request.form.get('sensacao_desmaio') == 'sim'
        insonia = request.form.get('insonia') == 'sim'
        olhos_lacrimejantes_cocando = request.form.get('olhos_lacrimejantes_cocando') == 'sim'
        olhos_inchados_vermelhos = request.form.get('olhos_inchados_vermelhos') == 'sim'
        olheiras = request.form.get('olheiras') == 'sim'
        visao_borrada = request.form.get('visao_borrada') == 'sim'
        coceira_ouvido = request.form.get('coceira_ouvido') == 'sim'
        dor_ouvido = request.form.get('dor_ouvido') == 'sim'
        retirada_fluido = request.form.get('retirada_fluido') == 'sim'
        zunido_ouvido = request.form.get('zunido_ouvido') == 'sim'
        nariz_entupido = request.form.get('nariz_entupido') == 'sim'
        sinusite = request.form.get('sinusite') == 'sim'
        corrimento_nasal = request.form.get('corrimento_nasal') == 'sim'
        espirro = request.form.get('espirro') == 'sim'
        coceira_olhos = request.form.get('coceira_olhos') == 'sim'
        ataque_espirro = request.form.get('ataque_espirro') == 'sim'
        muco_excessivo = request.form.get('muco_excessivo') == 'sim'
        tosse_cronica = request.form.get('tosse_cronica') == 'sim'
        dor_garganta = request.form.get('dor_garganta') == 'sim'
        necessidade_limpar_garganta = request.form.get('necessidade_limpar_garganta') == 'sim'
        rouquidao = request.form.get('rouquidao') == 'sim'
        lingua_gengiva_labio_inchado = request.form.get('lingua_gengiva_labio_inchado') == 'sim'
        acne = request.form.get('acne') == 'sim'
        perda_cabelo = request.form.get('perda_cabelo') == 'sim'
        suor_excessivo = request.form.get('suor_excessivo') == 'sim'
        feridas_cocam = request.form.get('feridas_cocam') == 'sim'
        pele_seca = request.form.get('pele_seca') == 'sim'
        vermelhidao = request.form.get('vermelhidao') == 'sim'
        calor_excessivo = request.form.get('calor_excessivo') == 'sim'
        batida_irregular_coracao = request.form.get('batida_irregular_coracao') == 'sim'
        batidas_rapidas_demais_coracao = request.form.get('batidas_rapidas_demais_coracao') == 'sim'
        dor_peito = request.form.get('dor_peito') == 'sim'
        dor_cabeca = request.form.get('dor_cabeca') == 'sim'
        data = datetime.now()

        insert_query = '''INSERT INTO rastreamento_metabolico (
                            tontura, sensacao_desmaio, insonia, olhos_lacrimejantes_cocando, 
                            olhos_inchados_vermelhos, olheiras, visao_borrada, coceira_ouvido, 
                            dor_ouvido, retirada_fluido, zunido_ouvido, nariz_entupido, 
                            sinusite, corrimento_nasal, espirro, coceira_olhos, ataque_espirro, 
                            muco_excessivo, tosse_cronica, dor_garganta, necessidade_limpar_garganta, 
                            rouquidao, lingua_gengiva_labio_inchado, acne, perda_cabelo, suor_excessivo, 
                            feridas_cocam, pele_seca, vermelhidao, calor_excessivo, batida_irregular_coracao, 
                            batidas_rapidas_demais_coracao, dor_peito, dor_cabeca, data
                          ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        
        cursor.execute(insert_query, (
            tontura, sensacao_desmaio, insonia, olhos_lacrimejantes_cocando, 
            olhos_inchados_vermelhos, olheiras, visao_borrada, coceira_ouvido, 
            dor_ouvido, retirada_fluido, zunido_ouvido, nariz_entupido, 
            sinusite, corrimento_nasal, espirro, coceira_olhos, ataque_espirro, 
            muco_excessivo, tosse_cronica, dor_garganta, necessidade_limpar_garganta, 
            rouquidao, lingua_gengiva_labio_inchado, acne, perda_cabelo, suor_excessivo, 
            feridas_cocam, pele_seca, vermelhidao, calor_excessivo, batida_irregular_coracao, 
            batidas_rapidas_demais_coracao, dor_peito, dor_cabeca, data
        ))
        cursor.execute("SELECT LASTVAL();")
        id_metabolico = cursor.fetchone()[0]
        conn.commit()

        insert_query = '''INSERT INTO paciente_metabolico (
            id_usuario, id_metabolico, data
        ) VALUES (%s, %s, %s);'''

        cursor.execute(insert_query, (
            id_usuario, id_metabolico, data
        ))

        conn.commit()

        print("Registro metabólico cadastrado com sucesso!")
        return redirect(url_for('auth.anthropometry'))

    except Exception as e:
        conn.rollback()
        print(f"Erro ao cadastrar registro metabólico: {e}")
        return jsonify({"error": "Erro ao cadastrar registro metabólico"}), 500

    finally:
        cursor.close()
        conn.close()

@auth.route("/anthropometry")
@login_required
def anthropometry():
    return render_template("public/templates/anthropometry.html")

@auth.route("/anthropometry_post", methods=["POST"])
@login_required
def anthropometry_post():
    conn, cursor = get_db_connection()
    
    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    id_usuario = current_user.id
    altura = request.form.get('altura')
    peso_atual = request.form.get('peso_atual')
    peso_ideal = request.form.get('peso_ideal')
    nivel_atividade = request.form.get('nivel_atividade')
    data = datetime.now()

    insert_query = '''INSERT INTO antropometria (data, altura, peso_ideal, peso_atual, nivel_atividade)
    VALUES (%s, %s, %s, %s, %s)'''

    cursor.execute(insert_query, (data, altura, peso_atual, peso_ideal, nivel_atividade))
    cursor.execute("SELECT LASTVAL();")
    id_antropometria = cursor.fetchone()[0]
    conn.commit()

    insert_query = '''INSERT INTO paciente_antropometria (
        id_usuario, id_antropometria, data
        ) VALUES (%s, %s, %s);'''

    cursor.execute(insert_query, (
        id_usuario, id_antropometria, data
    ))

    conn.commit()

    print("Registro antropométrico cadastrado com sucesso!")
    return redirect(url_for('auth.home'))