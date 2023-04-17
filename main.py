from base64 import b64decode
from pathlib import Path
import requests, json, time, csv
from datetime import date
from sendMail import envioEmail


# Parametros geral de emissão
datahoje = date.today()
vencimento = "2021-08-16"
mensagem = "Boleto referente ao mes de agosto."
nome_arquivo = "08-2021-"

# Importação dos dados
dados = []
with open('./pagadores/pagadores.csv') as csvfile:
    csvReader = csv.reader(csvfile)
    for row in csvReader:
        dados.append(row)

################################

def list_boletos():
    url = 'https://apis.bancointer.com.br/openbanking/v1/certificado/boletos?'
    header  = {'x-inter-conta-corrente': '49607405'}
    parametros = {'dataInicial': '2021-05-20', 'dataFinal': '2021-06-20'}
    request = requests.get(url, headers=header, params=parametros, cert=('./certificado/API_Certificado.crt', './certificado/API_Chave.key'))
    return (request.content)

def emite_boleto(apartamento):
    
    apto_posicao = 0
    for i in range (len(dados)):
        if apartamento in dados[i][0]:
            apto_posicao = i
            break
    if apto_posicao == 0:
        print ("Apartamento não localizado no arquivo")
        return 0

    url = 'https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos'
    headers  = {'x-inter-conta-corrente': '49607405', 'accept': 'application/json', 'content-type': 'application/json'}
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
        "seuNumero": datahoje.strftime("%Y%m")+apartamento,
        "dataLimite": "SESSENTA",
        "dataVencimento": vencimento,
        "mensagem": {
            "linha1": mensagem
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
        "cnpjCPFBeneficiario": "00000000000000",
        "numDiasAgenda": "TRINTA"  
    })

    request = requests.request("POST", url, headers=headers, data=payload, cert=('./certificado/API_Certificado.crt', './certificado/API_Chave.key'))
    print("\nImprimindo request text "+request.text)
    nossoNumero = (json.loads(request.content).get("nossoNumero"))
    file = (nome_arquivo+apartamento+".pdf")
    print ("\nGeracao de boleto OK, chamando Imprime Boleto")
    time.sleep(5)
    imprime_boleto(nossoNumero, file)
    #envioEmail((json.loads(payload).get("pagador")["email"]), (json.loads(payload).get("pagador")["nome"]), vencimento, file)

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



#https://developers.bancointer.com.br/reference#post_boletos
#https://documenter.getpostman.com/view/316127/T1LFoWF1?version=latest#f8741a60-ffcf-4066-afc9-62c84e13f4eb
#https://www.treinaweb.com.br/blog/consumindo-apis-com-python-parte-1/
