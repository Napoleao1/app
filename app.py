import json
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Funções para carregar e salvar a lista de compras
def salvar_lista(lista, arquivo="lista_compras.json"):
    with open(arquivo, "w") as f:
        json.dump(lista, f)

def carregar_lista(arquivo="lista_compras.json"):
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Função para adicionar item na lista
@app.route('/adicionar', methods=['POST'])
def adicionar_item():
    nome = request.form['nome']
    try:
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])
        if quantidade <= 0 or preco < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Quantidade ou preço inválidos!"}), 400

    lista_compras = carregar_lista()
    lista_compras.append({"nome": nome, "quantidade": quantidade, "preco": preco})
    salvar_lista(lista_compras)
    return redirect(url_for('index'))

# Função para remover item
@app.route('/remover/<int:index>', methods=['GET'])
def remover_item(index):
    lista_compras = carregar_lista()
    if 0 <= index < len(lista_compras):
        lista_compras.pop(index)
        salvar_lista(lista_compras)
    return redirect(url_for('index'))

# Página principal para exibir a lista de compras
@app.route('/')
def index():
    lista_compras = carregar_lista()
    total = sum(item['quantidade'] * item['preco'] for item in lista_compras)
    return render_template('index.html', lista_compras=lista_compras, total=total)

# Página para limpar a lista
@app.route('/limpar', methods=['GET'])
def limpar_lista():
    salvar_lista([])  # Limpar a lista
    return redirect(url_for('index'))

# Página para salvar a lista (essa função é apenas ilustrativa)
@app.route('/salvar', methods=['GET'])
def salvar():
    lista_compras = carregar_lista()
    salvar_lista(lista_compras)
    return jsonify({"status": "success", "message": "Lista salva com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
