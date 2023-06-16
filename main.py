from flask import Flask, render_template, request, redirect
import requests
import json

app = Flask(__name__)

api = 'http://localhost:5000'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/formRemoverProduto')
def formRemoverProduto():
    return render_template('formRemoverProduto.html')

@app.route('/formAdicionarProduto')
def formAdicionarProduto():
    return render_template('formAdicionarProduto.html')

@app.route('/adicionarProduto')
def adicionarProduto():
    data = int(request.args.get('codigo'))
    quantidade = int(request.args.get('quantidade'))
    response = requests.get(f'{api}/receberProduto?codigo={data}&quantidade={quantidade}')
    if response.text == 'produto nao encontrado':
            return render_template('formAdd.html', codigo = data)
    else:
        return redirect('/formAdicionarProduto')
    
@app.route('/removerProduto')
def removerProduto():
    data = request.args.get('codigo')
    quantidade = request.args.get('quantidade')
    response = requests.get(f'{api}/saidaProduto?codigo={data}&quantidade={quantidade}')
    if response.text == 'produto nao encontrado':
            return render_template('formAdd.html', codigo = data)
    else:
        return redirect('/formRemoverProduto')


@app.route('/estoqueBaixo')
def estoqueBaixo():
    data = requests.get(f'{api}/all')
    data_dict = data.json()
    estoquebaixo=[]
    for x in data_dict:
        if int(x.get('quantidade'))<20:
            estoquebaixo.append(x)
    if estoquebaixo.__len__ !=0:
        return render_template("searchResults.html", dados=estoquebaixo, tamanho=len(estoquebaixo), back="/")


@app.route('/formAdd')
def formAdd():
    return render_template('formAdd.html', codigo = None)


@app.route('/addProduto', methods=['POST'])
def addProduto():
    data = request.form.to_dict()
    requests.post(f'{api}/addProduto', json=json.dumps(data))
    return redirect('/')


@app.route('/formSearchCodigo')
def formSearchCodigo():
    return render_template('formSearchCodigo.html')


@app.route('/searchCodigo')
def searchCodigo():
    produto = []
    form = request.args.get('codigo')
    data = requests.get(f'{api}/pesquisarCodigo?codigo={form}')
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
    data = requests.get(f'{api}/pesquisarNome?nome={form}')
    if data.json() != 0:
        data_dict = data.json()
        produto.append(data_dict)
        if type(data.json()) == type(produto):
            return render_template('searchResults.html', dados=data_dict, tamanho=len(data_dict), back='/formSearchNome')
        else:
            return render_template('searchResults.html', dados=produto, tamanho=len(produto), back='/formSearchNome')
    else:
        return render_template('nameNotFound.html')


@app.route('/all')
def mostrarTodos():
    data = requests.get(f'{api}/all')
    if data.json() != 0:
        data_dict = data.json()
        for x in range(0, len(data_dict)):
            data_dict[x]['preco'] = format(float(data_dict[x]['preco']), '.2f')
        return render_template("searchResults.html", dados=data_dict, tamanho=len(data_dict), back="/")
