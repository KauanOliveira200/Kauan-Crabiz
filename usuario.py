from conexao import Conexao
from hashlib import sha256

class Usuario() :
    def __init__(self) -> None:
        self.nome = None
        self.telefone = None
        self.senha = None
        self.logado = False
        
    def cadastrar(self,nome, telefone, senha) :
        
        #criptografando a senha
        senha = sha256(senha.encode()).hexdigest()
        
        try:            
            #conectando no banco de dados
            mydb = Conexao.conectar()
            
            mycursor = mydb.cursor()
            
            #FORMA 1
            sql = "INSERT INTO tb_usuario (nome, tel, senha) VALUES (%s, %s, %s)"
            val = (nome, telefone, senha)
            mycursor.execute(sql, val)
            
            #FORMA 2
            # sql = f"INSERT INTO tb_usuario (nome, tel, senha) VALUES ('{nome}', '{telefone}', '{senha}')"
            # mycursor.execute(sql)
            
            mydb.commit()
            
            self.nome = nome
            self.telefone = telefone
            self.senha = senha
            self.logado = True
            
            return True
        
        except:
            return False
        
        
    def logar(self, telefone, senha):
        
        #criptografando a senha
        senha = sha256(senha.encode()).hexdigest()
         
        mydb = Conexao.conectar()
        
        mycursor = mydb.cursor()
        
        #FORMA 1
        sql = "SELECT nome, tel, senha FROM tb_usuario where tel = %s and BINARY senha = %s;"
        valores = (telefone, senha)
        mycursor.execute(sql,valores)
        
        # FORMA 2
        # sql = f"SELECT * FROM tb_usuario where tel = ' ' and senha = '{senha}';"
        # mycursor.execute(sql)
     
        resultado = mycursor.fetchone()
        
        if resultado != None:
            self.logado = True
            self.nome = resultado[0]
            self.telefone = resultado[1]
            self.senha = resultado[2]
        else:
            self.logado = False
            

