from utils import *
import psycopg2
from flask import Response, request, jsonify, session, render_template, flash, Blueprint, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
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
    if current_user.is_authenticated:
        return render_template("public/templates/home.html")

@auth.route("/login")
def render_login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    error = request.args.get('error')
    return render_template("public/templates/login.html", error=error)

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
        senha = request.form.get('password')
        nome = request.form.get('nome')
        data_nascimento = request.form.get('data_nascimento')
        sexo = request.form.get('sexo')
        gestante = request.form.get('gestante')
        telefone = request.form.get('telefone')
        cpf = request.form.get('Cpf')
        cep = request.form.get('Cep')
        rua = request.form.get('Rua')
        numero = request.form.get('Numero')
        bairro = request.form.get('Bairro')
        cidade = request.form.get('Cidade')
        uf = request.form.get('UF')
        
        query = '''SELECT cpf FROM paciente WHERE cpf = %s;'''
        cursor.execute(query, (cpf,))
        user = cursor.fetchone()

        if user:
            print("CPF já cadastrado")
            return redirect(url_for('auth.signup'))
        
        insert_query = '''INSERT INTO paciente (email, senha, nome, data_nascimento, sexo, gestante, telefone, cpf, cep, rua, numero, bairro, cidade, uf)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        cursor.execute(insert_query, (email, generate_password_hash(senha), nome, data_nascimento, sexo, gestante, telefone, cpf, cep, rua, numero, bairro, cidade, uf))
        conn.commit()

        print("Usuário cadastrado com sucesso!")
        return redirect(url_for('auth.login'))

    except Exception as e:
        print("Erro ao cadastrar usuário: " + str(e))
        return redirect(url_for('auth.signup'))
    

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("public/index.html")