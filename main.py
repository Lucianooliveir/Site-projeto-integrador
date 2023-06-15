from flask import Flask, render_template, request, redirect
import requests
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/formAdd')
def formAdd():
    return render_template('formAdd.html')


@app.route('/addProduto', methods=['POST'])
def addProduto():
    data = request.form.to_dict()
    print(json.dumps(data))
    requests.post('http://127.0.0.1:5000/addProduto', json=json.dumps(data))
    return redirect('/')


@app.route('/formSearchCodigo')
def formSearchCodigo():
    return render_template('formSearchCodigo.html')


@app.route('/searchCodigo')
def searchCodigo():
    produto = []
    form = request.args.get('codigo')
    data = requests.get(f'http://127.0.0.1:5000/pesquisarCodigo?codigo={form}')
    if data.json() != 0:
        data_dict = data.json()
        produto.append(data_dict)
        return render_template('searchResults.html', dados=produto, tamanho=len(produto), back='/formSearchCodigo')
    else:
        return render_template('codeNotFound.html')


@app.route('/formSearchNome')
def formSearchNome():
    return render_template('formSearchNome.html')


@app.route('/searchNome')
def searchNome():
    produto = []
    form = request.args.get('nome')
    data = requests.get(f'http://127.0.0.1:5000/pesquisarNome?nome={form}')
    if data.json() != 0:
        data_dict = data.json()
        produto.append(data_dict)
        return render_template('searchResults.html', dados=produto, tamanho=len(produto), back='/formSearchNome')
    else:
        return render_template('nameNotFound.html')


@app.route('/all')
def mostrarTodos():
    teste = requests.get('http://brasilapi.simplescontrole.com.br/mercadoria/consulta/?ean=7894900700046&access-token=51C7VNFHTVXYPSZFovlAVHBoWiFLpK6u&_format=json')
    print(teste.json())
    data = requests.get('http://127.0.0.1:5000/all')
    data_dict = data.json()
    for x in range(0, len(data_dict)):
        data_dict[x]['preco'] = format(float(data_dict[x]['preco']), '.2f')
    return render_template("searchResults.html", dados=data_dict, tamanho=len(data_dict), back="/")
