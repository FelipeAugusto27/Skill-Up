from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Iniciando app
app = Flask(__name__)

# Conexão com Banco
def get_db_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "alunolab",
        database = "teste",
        port = 3303
    )

# Chamando a conexão para variavel con
con = get_db_connection()
# Jogando a conexão para a variavel cursor

cursor = con.cursor()

nome = "Administrador"
email = "Administrador@email.com"
usuario = "Admin"
senha = "Admin123"
tipo = "admin"
pontos = "NULL"

# Pesquisando no banco de dados
cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))

# Perguntando se não encontrou ninguém cadastrado
if cursor.fetchone() is None:
    sql = "INSERT INTO usuarios (nome, email, usuario, senha, tipo) VALUES(%s, %s, %s, %s, %s)"
    valores = (nome, email, usuario, senha, tipo) 
    cursor.execute(sql, valores) 
    con.commit()
    
cursor.close()
con.close()

# Caminho para página de login
@app.route("/")
def login():
    error = request.args.get('error')
    return render_template("login.html", error=error)

#Rota para logar
@app.route("/logar", methods = ["GET", "POST"])
def logar ():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    if not usuario or not senha:
        return redirect(url_for("login", error="Preencher todos os campos"))
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND senha=%s", (usuario, senha))
    user = cursor.fetchone()
    cursor.close
    con.close
    if user:
        if user["tipo"] == "admin":
            return redirect(url_for("navadmin"))
        else:
            return redirect(url_for("navusuario"))
    else:
        return redirect(url_for("login", error="Usuário ou Senha inválidos"))

#Rotas após o login
#Tabela do admin
@app.route("/admin")
def pagina_admin():
    search = request.args.get('search', '')
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    if search:
        cursor.execute("SELECT usuario, email, pontos FROM usuarios WHERE usuario LIKE %s OR email LIKE %s", ('%' + search + '%', '%' + search + '%'))
    else:
        cursor.execute("SELECT usuario, email, pontos FROM usuarios")

    usuarios = cursor.fetchall()

    cursor.close()
    con.close()

    return render_template("pagina_admin.html", usuarios=usuarios, search=search)
#Usuários comuns
@app.route("/usuario")
def pagina_usuario():
    return render_template("pagina_usuario.html")

#Rota para tela de navegação do admin
@app.route("/navadmin")
def navadmin():
    return render_template("navadmin.html")

#Rota para tela de navegação do usuario
@app.route("/navusuario")
def navusuario():
    return render_template("navusuario.html")

#Rota para o jogo
@app.route("/jogo")
def jogo():
    return render_template("jogo.html")

# Caminho para página de cadastro
@app.route("/cadastrar", methods=["GET","POST"])
def cadastrar():
    # Pegando informações do formulário
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        tipo = request.form.get("tipo") or "user"
        pontos = "NULL"

        if not nome or not email or not usuario or not senha:
            return "Campos obrigatórios"
        con = get_db_connection()
        cursor = con.cursor()
        # Executando o SELECT para verificar se email e usuário já existem
        cursor.execute("SELECT * FROM usuarios WHERE email=%s or usuario=%s", (email, usuario))
        if cursor.fetchone():
            cursor.close()
            con.close()
            return "Email ou Usuário já cadastrado"
        #Instrução de inserção no banco de dados
        sql = "INSERT INTO usuarios (nome, email, usuario, senha, tipo, pontos) VALUES (%s, %s, %s, %s, %s, NULL)"
        valores = (nome, email, usuario, senha, tipo)
        cursor.execute(sql, valores)
        con.commit()
        # Retorno se tiver exito
        return redirect(url_for("login"))
    
    return render_template("login.html")

# Finalizar meu app
if __name__ == "__main__":
    app.run(debug=True)
