from flask import Flask, render_template,request, jsonify, session, redirect
from usuario import Usuario
from chat import Chat
from contato import Contato

app = Flask(__name__)

app.secret_key = "batatinhafrita123"


#Rota GET para o index ou cadastro
@app.route("/")
@app.route("/cadastro_via_form")
def pag_cadastro():
    return render_template("cadastro_via_form.html")

#Rota POST para o cadastro, ele pega os dados enviados via formulario
@app.route("/cadastro_via_form", methods=["POST"])
def post_cadastro():
    #Pegando os dados do form
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    senha = request.form["senha"]

    #Instanciando o objeto usuário
    usuario = Usuario()
    
    #Cadastrando e retornando se deu certo ou não
    if usuario.cadastrar(nome, telefone, senha) == True:
        
        session['usuario_logado'] = {"nome":usuario.nome,
                                     "telefone":usuario.telefone}
        
        return "Cadastro efetuado com sucesso!"
    else:
        session.clear()
        
        return "Erro ao cadastrar"
    
    
    
    

#Rota GET para outra página de cadastro, essa realiza o cadastro usando requisição via post
@app.route("/cadastrar_via_ajax")
def pag_cadastro_ajax():
    return render_template("cadastro_via_ajax.html")



 
#Rota POST para o cadastro, ele pega os dados enviados via AJAX
@app.route("/cadastrar_via_ajax", methods=["POST"])
def post_cadastro_ajax():
    #Pegando os dados que foram enviados
    dados = request.get_json()
    
    nome = dados["nome"]
    telefone = dados["telefone"]
    senha = dados["senha"]
    
     #Instanciando o objeto usuário
    usuario = Usuario()
    
    #Cadastrando e retornando se deu certo ou não
    if usuario.cadastrar(nome, telefone, senha) == True:
        return jsonify({'mensagem':'Cadastro OK'}), 200
    else:
        return jsonify({'mensagem':'ERRO'}), 500
    
    
    
    
#Rota GET para mostrar a tela de login
@app.route("/login")
def pag_login():
    return render_template("login.html")



#Rota POST para verificar o usuário
@app.route("/login", methods=["POST"])
def pag_login_post():
    telefone = request.form["telefone"]
    senha = request.form["senha"]
    
    usuario = Usuario()
    
    usuario.logar(telefone,senha)
    
    if usuario.logado == True:
        session['usuario_logado'] = {"nome":usuario.nome,
                                     "telefone":usuario.telefone}
        return redirect("/chat")
    else:
        return redirect("/login")
    

#Rota GET para abrir a tela do chat se o usuário já estiver logado
@app.route("/chat")
def pag_chat():
    if "usuario_logado" in session :
        return render_template("chat.html")
    else:
        return redirect("/cadastro_via_form")



#Rota GET para retornar os usuários cadastrados em formato de JSON
@app.route("/retorna_usuarios")
def retorna_usuarios():
    
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario,telefone_usuario)
    
    contatos = chat.retornar_contatos()
    
    return jsonify(contatos), 200
    
        

@app.route("/get/usuarios")
def api_get_usuarios():
    chat = Chat(nome_usuario,telefone_usuario)
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    contatos = chat.retornar_contatos()

    return jsonify(contatos), 200

@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    chat= Chat(nome_usuario,telefone_usuario)

    contato_destinatario = Contato("",tel_destinatario)

    lista_de_mensagem = chat.verificar_mensagem(0,contato_destinatario)

    return jsonify(lista_de_mensagem), 200

# Dicionário para armazenar as mensagens (simulando um banco de dados)
mensagens = {}

# @app.route("/enviar_mensagem/<tel_destinatario>", methods=["POST"])
# def enviar_mensagem(tel_destinatario):
#     if "usuario_logado" in session:
#         mensagem = request.get_json()["mensagem"]
#         remetente = session["usuario_logado"]["telefone"]

#         if tel_destinatario not in mensagens:
#             mensagens[tel_destinatario] = []

#         mensagens[tel_destinatario].append({"remetente": remetente, "mensagem": mensagem})

#         return jsonify({"mensagem": "Mensagem enviada com sucesso"}), 200
#     else:
#         return jsonify({"mensagem": "Usuário não está logado"}), 401

# Rota para o envio de mensagem via AJAX
@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem_ajax():
    if request.method == "POST":
        # Recebe os dados da requisição AJAX
        dados = request.json
        destinatario = dados["destinatario"]
        mensagem = dados["mensagem"]

        # Obtém o nome e o telefone do usuário logado na sessão
        nome_usuario = session["usuario_logado"]["nome"]
        telefone_usuario = session["usuario_logado"]["telefone"]
        
        # Instancia um objeto Chat para interagir com os contatos e mensagens
        chat = Chat(nome_usuario, telefone_usuario)
        # Cria um objeto Contato com o telefone do destinatário
        contato_destinatario = Contato("", destinatario)
        envia = chat.enviar_mensagem(mensagem,contato_destinatario)
        return jsonify({"status": "Mensagem enviada com sucesso"}), 200
    else:
       
        return jsonify({"status": "Erro ao enviar mensagem"}), 5000


app.run(debug=True)
