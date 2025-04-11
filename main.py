# projeto_microplasticos/main.py

import subprocess
import threading
import time
import random
import requests
from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS

# --- Inicializa o servidor MongoDB ---
def iniciar_mongodb():
    subprocess.Popen([
    "C:/Program Files/MongoDB/Server/8.0/bin/mongod.exe",
    "--dbpath", "D:/Documents/FIAP/projeto_microplasticos/database"
])

# --- Simulador de Sensor ---
def sensor_simulado():
    while True:
        valor = random.randint(50, 1000)
        status = 1 if valor < 300 else 0
        try:
            requests.post("http://localhost:5000/dados", json={"valor": valor, "status": status})
            print(f"Enviado: Luminosidade={valor}, Status={status}")
        except:
            print("Erro ao enviar dados")
        time.sleep(30)  # Alterado para 30 segundos

# --- Backend Flask ---
app = Flask(__name__)
CORS(app)
client = MongoClient('localhost', 27017)
db = client['microplasticos']
coleta = db['leituras']

@app.route('/dados', methods=['POST'])
def receber_dados():
    data = request.json
    data['data_hora'] = datetime.now()
    coleta.insert_one(data)
    return jsonify({'status': 'ok'})

@app.route('/dados', methods=['GET'])
def listar_dados():
    dados = list(coleta.find({}, {'_id': 0}))
    return jsonify(dados)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - Microplásticos</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: Arial; padding: 20px; }
            canvas { max-width: 100%; max-height: 500px; }
            #tempo-range { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h2>Monitoramento de Luminosidade</h2>
        <canvas id="grafico"></canvas>
        <div id="tempo-range">
            <label for="intervalo">Intervalo de tempo (segundos): </label>
            <input type="range" id="intervalo" min="10" max="120" step="10" value="30" oninput="atualizarIntervalo(this.value)">
            <span id="intervalo-valor">30</span>s
        </div>
        <script>
            let chart;
            let intervalo = 3000;

            async function carregarDados() {
                const response = await fetch('/dados');
                const dados = await response.json();

                const valores = dados.map(d => d.valor);
                const tempos = dados.map(d => new Date(d.data_hora).toLocaleTimeString());
                const cores = dados.map(d => d.status === 1 ? 'red' : 'green');

                const ponto = {
                    label: 'Luminosidade',
                    data: valores,
                    borderColor: 'rgba(0, 0, 0, 0.1)',
                    pointBackgroundColor: cores,
                    pointRadius: 5,
                    fill: false
                };

                if (chart) {
                    chart.data.labels = tempos;
                    chart.data.datasets[0] = ponto;
                    chart.update();
                } else {
                    chart = new Chart(document.getElementById('grafico'), {
                        type: 'line',
                        data: {
                            labels: tempos,
                            datasets: [ponto]
                        },
                        options: {
                            responsive: true,
                            scales: {
                                x: {
                                    ticks: {
                                        autoSkip: true,
                                        maxTicksLimit: 10
                                    }
                                },
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                }
            }

            function atualizarIntervalo(valor) {
                document.getElementById('intervalo-valor').innerText = valor;
                intervalo = valor * 1000;
                clearInterval(intervaloAtualizacao);
                intervaloAtualizacao = setInterval(carregarDados, intervalo);
            }

            carregarDados();
            let intervaloAtualizacao = setInterval(carregarDados, intervalo);
        </script>
    </body>
    </html>
    ''')

# --- Inicialização ---
if __name__ == '__main__':
    print("Iniciando MongoDB...")
    threading.Thread(target=iniciar_mongodb).start()
    time.sleep(5)  # Tempo para o Mongo subir

    print("Iniciando sensor simulado...")
    threading.Thread(target=sensor_simulado, daemon=True).start()

    print("Iniciando servidor Flask...")
    app.run(debug=True)
