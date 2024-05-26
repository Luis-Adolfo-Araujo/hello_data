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
        query = '''SELECT cpf FROM paciente WHERE cpf = %s OR email = %s OR telefone = %s;'''
        cursor.execute(query, (cpf, email, telefone))
        user = cursor.fetchone()

        if user:
            error_message = "Usuário ja cadastrado"
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

    cursor.execute(insert_query, (data, altura, peso_ideal, peso_atual, nivel_atividade))
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

@auth.route("/get_anamnesis")
@login_required
def get_patient_anamnesis():
    conn, cursor = get_db_connection()
    
    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    try:
        query = """
        SELECT 
            p.User_id,
            p.nome,
            p.sexo,
            p.gestante,
            ip.objetivo,
            ip.resticao_alimentar,
            ip.ingere_alcool,
            ip.dorme_bem,
            ip.horas_sono,
            ip.pratica_exercicios,
            ip.patologia,
            ip.Medicamentos,
            ip.apetite,
            ip.mastigacao,
            ip.habito_intestinal,
            ip.frequencia_evacuacao,
            ip.formato_fezes,
            ip.usa_laxante,
            ip.cor_fezes,
            ip.ingestao_hidrica,
            ip.sintomas,
            rm.tontura,
            rm.sensacao_desmaio,
            rm.insonia,
            rm.olhos_lacrimejantes_cocando,
            rm.olhos_inchados_vermelhos,
            rm.olheiras,
            rm.visao_borrada,
            rm.coceira_ouvido,
            rm.dor_ouvido,
            rm.retirada_fluido,
            rm.zunido_ouvido,
            rm.nariz_entupido,
            rm.sinusite,
            rm.corrimento_nasal,
            rm.espirro,
            rm.coceira_olhos,
            rm.ataque_espirro,
            rm.muco_excessivo,
            rm.tosse_cronica,
            rm.dor_garganta,
            rm.necessidade_limpar_garganta,
            rm.rouquidao,
            rm.lingua_gengiva_labio_inchado,
            rm.acne,
            rm.perda_cabelo,
            rm.suor_excessivo,
            rm.feridas_cocam,
            rm.pele_seca,
            rm.vermelhidao,
            rm.calor_excessivo,
            rm.batida_irregular_coracao,
            rm.batidas_rapidas_demais_coracao,
            rm.dor_peito,
            rm.dor_cabeca,
            rm.data AS data_metabolico,
            a.data AS data_antropometria,
            a.altura,
            a.peso_atual,
            a.peso_ideal,
            a.nivel_atividade
        FROM 
            paciente p
        LEFT JOIN 
            info_paciente ip ON p.User_id = ip.id_usuario
        LEFT JOIN 
            paciente_metabolico pm ON p.User_id = pm.id_usuario
        LEFT JOIN 
            rastreamento_metabolico rm ON pm.id_metabolico = rm.Id_metabolico
        LEFT JOIN 
            paciente_antropometria pa ON p.User_id = pa.id_usuario
        LEFT JOIN 
            antropometria a ON pa.id_antropometria = a.id_antropometria
        WHERE 
            p.User_id = %s
        """
        
        cursor.execute(query, (current_user.id,))
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        anamnesis_data = [dict(zip(columns, row)) for row in result]

        cursor.close()
        conn.close()

        if any(value is None for row in anamnesis_data for value in row.values()):
            print('Você não possui uma anamnese cadastrada.')
            return jsonify(None)

        return jsonify(anamnesis_data)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500


@auth.route("/second_join")
@login_required
def get_patient_anamnesis_simplified():
    conn, cursor = get_db_connection()
    
    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    try:
        query = """
        SELECT 
            p.User_id,
            p.nome,
            p.sexo,
            p.gestante,
            ip.objetivo,
            ip.resticao_alimentar,
            ip.ingere_alcool,
            ip.dorme_bem,
            ip.horas_sono,
            ip.pratica_exercicios,
            ip.patologia,
            ip.Medicamentos,
            ip.apetite,
            ip.mastigacao,
            ip.habito_intestinal,
            ip.frequencia_evacuacao,
            ip.formato_fezes,
            ip.usa_laxante,
            ip.cor_fezes,
            ip.ingestao_hidrica,
            a.data AS data_antropometria,
            a.altura,
            a.peso_atual,
            a.peso_ideal,
            a.nivel_atividade
        FROM 
            paciente p
        LEFT JOIN 
            info_paciente ip ON p.User_id = ip.id_usuario
        LEFT JOIN 
            paciente_antropometria pa ON p.User_id = pa.id_usuario
        LEFT JOIN 
            antropometria a ON pa.id_antropometria = a.id_antropometria
        """
        
        cursor.execute(query, (current_user.id,))
        result = cursor.fetchall()
        print(result)

        cursor.close()
        conn.close()

        return jsonify(result)

    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('auth.home'))

@auth.route('/anamnesis_summary', methods=["GET"])
@login_required
def anamnesis_summary():
    return render_template("public/templates/anamnesis_summary.html")

@auth.route('/delete_anamnesis', methods=["DELETE"])
@login_required
def delete_anamnesis():
    conn, cursor = get_db_connection()
    
    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        sql_query = """
        BEGIN;

        -- Excluir dados da tabela info_paciente
        DELETE FROM info_paciente
        WHERE id_usuario = %s;

        -- Excluir dados da tabela paciente_metabolico
        DELETE FROM paciente_metabolico
        WHERE id_usuario = %s;

        -- Excluir dados da tabela paciente_antropometria
        DELETE FROM paciente_antropometria
        WHERE id_usuario = %s;

        -- Excluir dados da tabela rastreamento_metabolico
        DELETE FROM rastreamento_metabolico
        WHERE Id_metabolico IN (SELECT id_metabolico FROM paciente_metabolico WHERE id_usuario = %s);

        -- Excluir dados da tabela antropometria
        DELETE FROM antropometria
        WHERE id_antropometria IN (SELECT id_antropometria FROM paciente_antropometria WHERE id_usuario = %s);

        COMMIT;
        """
        user_id = current_user.id
        cursor.execute(sql_query, (user_id, user_id, user_id, user_id, user_id))
        conn.commit()
        return jsonify({"message": "Anamnese deletada com sucesso!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@auth.route("/profile")
@login_required
def get_profile():
    conn, cursor = get_db_connection()
    
    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    query = '''SELECT * FROM paciente WHERE user_id = %s'''
    cursor.execute(query, (current_user.id,))
    paciente = cursor.fetchone()
    conn.commit()

    return render_template("public/templates/profile.html", paciente=paciente)

@auth.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    conn, cursor = get_db_connection()
    
    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        gestante = request.form.get('gestante') == 'True'
        cep = request.form.get('cep')
        rua = request.form.get('rua')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        uf = request.form.get('uf')

        query = '''
        UPDATE paciente
        SET email = %s, telefone = %s, gestante = %s, cep = %s, rua = %s, numero = %s, bairro = %s, cidade = %s, uf = %s
        WHERE user_id = %s
        '''
        
        cursor.execute(query, (email, telefone, gestante, cep, rua, numero, bairro, cidade, uf, current_user.id))
        conn.commit()
        
        return redirect(url_for('auth.home'))
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()