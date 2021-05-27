import requests
import csv
import ssl
import numpy as np
import json
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
    print(request.content)

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
        "dataEmissao": datahoje.strftime,
        "seuNumero": ""+datahoje.strftime("%d%m%y")+apartamento+"",
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

    
    print(payload)
    request = requests.request("POST", url, headers=headers, data=payload, cert=('./certificado/API_Certificado.crt', './certificado/API_Chave.key'))
    print(request.content)  
    print(request.text)
    print(request)           


#apartamento = emite_boleto('101')
list_boletos()


#https://developers.bancointer.com.br/reference#post_boletos
#https://documenter.getpostman.com/view/316127/T1LFoWF1?version=latest#f8741a60-ffcf-4066-afc9-62c84e13f4eb
#https://www.treinaweb.com.br/blog/consumindo-apis-com-python-parte-1/