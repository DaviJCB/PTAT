import re
import os
import socket


class PTATCLiente:
    def __init__(self):
        self.x = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.endereco_servidor = "localhost", 200

    def enviar_requisicao(self, requisicao):
        for i in requisicao:
            self.x.sendto(i.encode(), self.endereco_servidor)

    def receber_resposta(self):
        resposta = []
        for i in range(7):
            mensagem, endereco_servidor = self.x.recvfrom(4000000)
            mensagem = mensagem.decode()
            resposta.append(mensagem)
        return resposta

def pedir_comando():
    return input("Insira o comando: ")

def formatar_msg(msg):
    msg_separada = re.split(r'[/\s]+', msg)
    filename_remote = ""
    body = ""
    length = 0
    if msg_separada[0] == 'read': 
        op = '0'
        filename_remote = msg_separada[2]
        caminho_remote = msg_separada[1]
        length = ""
    elif msg_separada[0] == 'write':
        op = '1'
        caminho_local = msg_separada[1]
        filename_local = msg_separada[2]
        caminho_remote = msg_separada[3]
        filename_remote = msg_separada[4]
        file = open((caminho_local+"/"+filename_local), "r")
        body = file.read()
        length = len(body)
        file.close()
    elif msg_separada[0] == 'del':
        op = '2'
        caminho_remote = msg_separada[1]
        filename_remote = msg_separada[2]
    elif msg_separada[0] == 'list':
        op = '3'
        caminho_remote = msg_separada[1]
    return formatar_lista(op, length, filename_remote, caminho_remote, body)

def formatar_lista(op, length, filename, PATH, body):
    requisicao = [
        op,
        f"{length:0>6}",
        filename.ljust(64),
        PATH.ljust(128),
        body
    ]
    return requisicao

def Principal():
    cliente = PTATCLiente()
    while True:
        comando = pedir_comando()
        requisicao = formatar_msg(comando)
        cliente.enviar_requisicao(requisicao)
        resposta = cliente.receber_resposta()
        print(resposta[5])
        print(resposta[6])

Principal()

input()