import os
import socket
import datetime

class PTATServidor:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        endereco_servidor = "localhost", 200
        self.socket.bind(endereco_servidor)

    def loop(self):
        while True:
            requisicao = self.receber_requisicao()
            resposta = self.processar_requisicao(requisicao)
            self.enviar_resposta(resposta)

    def receber_requisicao(self):
        global endereco_cliente
        requisicao = []
        for i in range(5):
            mensagem, endereco_cliente = self.socket.recvfrom(4000000)
            mensagem = mensagem.decode()
            requisicao.append(mensagem)

        return requisicao

    def enviar_resposta(self, resposta):
        global endereco_cliente
        for mensagem in resposta:
            self.socket.sendto(mensagem.encode(), endereco_cliente)

    def processar_requisicao(self, requisicao):
        operacao = requisicao[0]
        caminho = remover_espacos(requisicao[3])
        arquivo = remover_espacos(requisicao[2])

        if operacao == "0":
            resposta = fileReader(caminho, arquivo)

        elif operacao == "1":
            corpo = requisicao[4]
            resposta = fileWrite(caminho, arquivo, corpo)

        elif operacao == "2":
            resposta = fileDelet(caminho, arquivo)

        elif operacao == "3":
            resposta = fileList(caminho)

        exibir_log(resposta)

        return resposta

def exibir_log(log):
    print(datetime.datetime.now().strftime("%H:%M:%S"), end=" ")
    print(log[0], end=" ")
    print(log[3], end=" ")
    print(log[4])

def remover_espacos(string):
    return string.replace(" ", "")

def formatar_lista(op, length, filename, PATH, code, message, body):
    requisicao = [
         op,
         f"{length:0>6}",
         filename.ljust(64),
         PATH.ljust(128),
         str(code),
         message.ljust(128),
         body
    ]
    return requisicao


def fileReader(path, filename):
    if os.path.exists(path):
        if os.path.exists(f"{path}/{filename}"):
            with open(f"{path}/{filename}", "r") as file:
                body = file.read()
                length = len(body)
                code = 0
                message = "Arquivo lido com sucesso"
            file.close()
        else:
            message = "Nome de arquivo não existente no servidor"
            code = 2
            body = ""
    else:
        message = "Caminho não existente no servidor"
        code = 1
        body = ""
    return formatar_lista("0", length, filename, path, code, message, body)



def fileList(PATH):
    if os.path.exists(PATH):
        if not os.listdir(PATH):
            print("Não há arquivos neste diretório")
        else:
            for arquivo in os.listdir(PATH):
                BODY = str(os.listdir(PATH))
            length = len(BODY)
            if length < 999999:
                CODE = 0
                message = "Arquivo lido com sucesso"
            else: 
                CODE = 3
                message = "Arquivos demais para serem listados."
    else:
        message = "Caminho não existente no servidor"
        CODE = 1
    return formatar_lista("1", length, "", PATH, CODE, message, BODY)

def fileList(PATH):
    if os.path.exists(PATH):
        if not os.listdir(PATH):
            print("Não há arquivos neste diretório")
        else:
            for arquivo in os.listdir(PATH):
                BODY = str(os.listdir(PATH))
            length = len(BODY)
            if length < 999999:
                CODE = 0
                message = "Arquivo lido com sucesso"
            else: 
                CODE = 3
                message = "Arquivos demais para serem listados."
    else:
        message = "Caminho não existente no servidor"
        CODE = 1
    return formatar_lista("1", length, "", PATH, CODE, message, BODY)

def fileDelet(PATH, fileName):
    if os.path.exists(PATH):
        if os.path.exists(PATH+"/"+fileName):
            os.remove(PATH+"/"+fileName)
            CODE = 0
            message = "Arquivo deletado com sucesso!"
        else:
            message = "Nome de arquivo não existente no servidor"
            CODE = 2   
    else:
        message = "Caminho não existente no servidor."
        CODE = 1
    return formatar_lista("2", 0, fileName, PATH, CODE, message, "")

def fileWrite(PATH, fileName, BODY):
    if os.path.exists(PATH):
        if os.path.exists(PATH+"/"+fileName):
            message = "Nome de arquivo já existente no servidor."
            CODE = 5 #Caso especial, arquivo já existente.
        else:
            with open(PATH+"/"+fileName, "w") as file:
                file.write(BODY)
            CODE = 0
            message = "Arquivo escrito com sucesso."   
    else:
        message = "Caminho não existente no servidor."
        CODE = 1
    return formatar_lista("3", 0, fileName, PATH, CODE, message, "")

server = PTATServidor()
server.loop()