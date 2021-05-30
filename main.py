from base64 import b64decode
from pathlib import Path
import requests, json
import csv
import ssl
import numpy as np
from datetime import date



# Parametros geral de emissão
datahoje = date.today()
vencimento = "2021-06-07"
################################

def list_boletos():
    url = 'https://apis.bancointer.com.br/openbanking/v1/certificado/boletos?'
    header  = {'x-inter-conta-corrente': '49607405'}
    parametros = {'dataInicial': '2021-05-20', 'dataFinal': '2021-06-20'}
    request = requests.get(url, headers=header, params=parametros, cert=('./certificado/API_Certificado.crt', './certificado/API_Chave.key'))
    return (request.content)

dados = []
with open('./pagadores/pagadores.csv') as csvfile:
    csvReader = csv.reader(csvfile)
    for row in csvReader:
        dados.append(row)

def func_pesquisa_posicao(posicao):
    pos_i = 0

    for i in range (len(dados)):
        if posicao in dados[i][0]:
            pos_i = i
            break
    return(pos_i)

def emite_boleto(apartamento):
    apto_posicao = func_pesquisa_posicao(apartamento)
    url = 'https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos'
    headers  = {
        'x-inter-conta-corrente': '49607405',
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    aux = {}
    payload = json.dumps({
        "pagador":{ 
            "cnpjCpf": dados[apto_posicao][1],
            "nome": dados[apto_posicao][2],
            "email": dados[apto_posicao][3],
            "telefone": dados[apto_posicao][4],
            "cep": dados[apto_posicao][5],
            "numero": dados[apto_posicao][6],
            "complemento": dados[apto_posicao][7],
            "bairro": dados[apto_posicao][8],
            "cidade": dados[apto_posicao][9],
            "uf": dados[apto_posicao][10],
            "endereco": dados[apto_posicao][11],
            "ddd": dados[apto_posicao][12],
            "tipoPessoa": dados[apto_posicao][13]
        },
        "dataEmissao": datahoje.strftime("%Y-%m-%d"),
        "seuNumero": ""+datahoje.strftime("%d%m%Y")+apartamento+"",
        "dataLimite": "SESSENTA",
        "dataVencimento": ""+vencimento+"",
        "mensagem": {
            "linha1": "Boleto referente ao mes de abril pago em maio."
        },
        "desconto1": {
            "codigoDesconto": "NAOTEMDESCONTO",
            "taxa": 0,
            "valor": 0,
            "data": ""
        },
        "desconto2": {
            "codigoDesconto": "NAOTEMDESCONTO",
            "taxa": 0,
            "valor": 0,
            "data": ""
        },
        "desconto3": {
            "codigoDesconto": "NAOTEMDESCONTO",
            "taxa": 0,
            "valor": 0,
            "data": ""
        },
        "valorNominal": 80,
        "valorAbatimento": 0,
        "multa": {
            "codigoMulta": "NAOTEMMULTA",
            "valor":0,
            "taxa":0
        },
        "mora": {
            "codigoMora": "ISENTO",
            "valor":0,
            "taxa":0
        },
        "cnpjCPFBeneficiario": "35801021000190",
        "numDiasAgenda": "TRINTA"  
    })

    request = requests.request("POST", url, headers=headers, data=payload, cert=('./certificado/API_Certificado.crt', './certificado/API_Chave.key'))
    print("Imprimindo request content")
    print(request.content)
    print("\nImprimindo request text")
    print(request.text)
    print("\nImprimindo request")
    print(request)
    print ("\n\n\nGeracao de boleto OK, chamando Imprime Boleto")
    #return (request.content)
    #return (""+datahoje.strftime("%d%m%y")+apartamento+"")
    nossoNumero = (json.loads(request.content).get("nossoNumero"))
    print ("\n\n\nEsse eh o NossoNumero: "+nossoNumero)
    file = (""+datahoje.strftime("%d%m%Y")+apartamento+".pdf")
    print ("\nEsse eh o nome do arquivo "+file)
    print ("\nGeracao de boleto OK, chamando Imprime Boleto")
    imprime_boleto(nossoNumero, file)
    print ("\nSaindo do imprime boleto e voltando para o Gera Boleto")


def imprime_boleto(nossoNumero, file):
    payload={}
    filename =  Path(file)
    url = 'https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos/'+nossoNumero+'/pdf'
    header  = {'x-inter-conta-corrente': '49607405', 'content-type': 'application/base64', 'content-type': 'application/json', }
    requisicao = requests.get(url, headers=header, data=payload, cert=('./certificado/API_Certificado.crt', './certificado/API_Chave.key'))
    bytes = b64decode(requisicao.text, validate=True)
    f = open(filename, 'wb')
    f.write(bytes)
    f.close()
    print ("Imprime Boleto OK")

emite_boleto('102')

# nossoNumero = (json.loads(retornoBoleto).get("nossoNumero"))
# print ("\n\n\nEsse eh o NossoNumero: "+nossoNumero)
# file = (""+datahoje.strftime("%d%m%y")+"102")
# print ("\nEsse eh o nome do arquivo "+file)
# imprime_boleto(nossoNumero, file)
# print ("\nSaindo do imprime boleto e voltando para o Gera Boleto")



#print (json.loads(list_boletos()).get("totalPages"))

# uva = jaca.get("content")
# print (uva.get("nossoNumero"))
#print (jaca.get("totalPages"))





#https://developers.bancointer.com.br/reference#post_boletos
#https://documenter.getpostman.com/view/316127/T1LFoWF1?version=latest#f8741a60-ffcf-4066-afc9-62c84e13f4eb
#https://www.treinaweb.com.br/blog/consumindo-apis-com-python-parte-1/