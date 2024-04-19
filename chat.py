from usuario import Usuario
from mensagem import Mensagem
from contato import Contato
from conexao import Conexao

class Chat:
    
    def __init__(self, nome_usuario:str, telefone_usuario:str):
        self.nome_usuario = nome_usuario
        self.telefone_usuario = telefone_usuario
        
    def enviar_mensagem(self, conteudo: str, destinatario:Contato) -> bool:
        try:
            #conectando no banco de dados
            mydb = Conexao.conectar()
            
            mycursor = mydb.cursor()
            
            #FORMA 1
            sql = "INSERT INTO tb_mensagem (tel_remetente, mensagem, tel_destinatario) VALUES (%s, %s, %s)"
            val = (self.telefone_usuario, conteudo, destinatario.telefone)
            mycursor.execute(sql, val)
            
            #FORMA 2
            # sql = f"INSERT INTO tb_mensagem (tel_remetente, mensagem, tel_destinatario) VALUES ('{self.usuario.telefone}', '{conteudo}','{destinatario.telefone})"
            # mycursor.execute(sql)
            
            mydb.commit()
            
            return True
        
        except:
            return False
        
    def verificar_mensagem(self,quantidade:int,destinatario:Contato):
        
        mydb = Conexao.conectar()
        
        mycursor = mydb.cursor()
        
        sql = f"SELECT nome, mensagem FROM tb_mensagem m " \
                f"INNER JOIN tb_usuario u " \
                f"ON m.tel_remetente = u.tel " \
                f"WHERE m.tel_remetente = '{self.telefone_usuario}' " \
                    f"AND m.tel_destinatario = '{destinatario.telefone}' "\
                    f"OR m.tel_remetente = '{destinatario.telefone}' " \
                    f"AND m.tel_destinatario = '{self.telefone_usuario}' "
        
        mycursor.execute(sql)
        
        resultado = mycursor.fetchall()
        
        lista_mensagens = []
        
        for linha in resultado:
            #Tudo numa linha só
            #lista_mensagens.append(Mensagem(linha[0],linha[1]))
            
            #Criando a mensagem primeiro e incluindo na lista
            mensagem = {"nome":linha[0],"mensagem":linha[1]}
            lista_mensagens.append(mensagem)
        
        return (lista_mensagens)
    
    def retornar_contatos(self): 
        
        mydb = Conexao.conectar()
        
        mycursor = mydb.cursor()
        
        sql = "SELECT nome, tel FROM tb_usuario ORDER BY nome"
        
        
        mycursor.execute(sql)
        
        resultado = mycursor.fetchall()
        
        lista_contatos = []
        
        #Inserindo o contato TODOS
        lista_contatos.append({"nome":"TODOS","telefone":""})
        
        for linha in resultado:
            #Criando a mensagem primeiro e incluindo na lista
            contato = {"nome":linha[0],"telefone":linha[1]}
            lista_contatos.append(contato)
        
        return (lista_contatos)