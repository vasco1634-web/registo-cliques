from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ------------------ BASE DE DADOS ------------------

def ligar_bd():
    conn = sqlite3.connect('base_dados.db')
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    conn = ligar_bd()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cliques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            botao TEXT,
            contador INTEGER,
            data TEXT,
            hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

criar_tabela()

# ------------------ CONTADOR DIÁRIO ------------------

def obter_contador_diario(data_hoje):
    conn = ligar_bd()
    resultado = conn.execute(
        "SELECT MAX(contador) FROM cliques WHERE data = ?",
        (data_hoje,)
    ).fetchone()
    conn.close()

    if resultado[0] is None:
        return 1
    else:
        return resultado[0] + 1

# ------------------ ROTAS ------------------

@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/clique', methods=['POST'])
def registar_clique():
    botao = request.json['botao']

    agora = datetime.now()
    data = agora.strftime('%Y-%m-%d')
    hora = agora.strftime('%H:%M')

    contador = obter_contador_diario(data)

    conn = ligar_bd()
    conn.execute(
        "INSERT INTO cliques (botao, contador, data, hora) VALUES (?, ?, ?, ?)",
        (botao, contador, data, hora)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "contador": contador,
        "data": data,
        "hora": hora
    })

# ------------------ EXECUÇÃO ------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
