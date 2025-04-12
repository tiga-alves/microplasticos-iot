# 🌊 Projeto IoT Simulado – Detecção de Microplásticos na Água

Este projeto simula um sistema de Internet das Coisas (IoT) para detectar microplásticos na água usando sensores e visualização em tempo real via dashboard. Mesmo sem hardware físico, o sistema reproduz todas as camadas de uma arquitetura IoT moderna: sensorial, comunicação, backend e aplicação.

---

## 📌 Objetivo

Conscientizar sobre a presença de microplásticos na água por meio de um protótipo digital capaz de identificar partículas com base em leitura de luminosidade simulada. O projeto faz parte do tema ODS 3 – **Saúde e Bem-Estar**.

---

## 🧱 Arquitetura

[Sensor Simulado] --> [Flask API REST] --> [MongoDB] --> [Dashboard Web]


- **Sensor simulado**: gera valores de luminosidade.
- **Flask (Python)**: recebe os dados e os armazena no banco.
- **MongoDB**: banco de dados NoSQL local.
- **HTML + Chart.js**: dashboard responsivo com visualização em tempo real.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.x
- Flask + Flask-CORS
- MongoDB Community Edition
- Chart.js
- HTML/CSS
- Threading / Subprocess
- REST API

---

## 📁 Estrutura do Projeto

```text
projeto_microplasticos/
├── main.py        # Script principal (sensor, backend, dashboard)
├── database/      # Pasta usada pelo MongoDB para persistência
├── README.md      # Documentação
```

---

## 🚀 Como Executar Localmente

### 1. Instale os Requisitos

> É recomendado usar um ambiente virtual (ex: `iotenv` com Anaconda ou venv)

```bash
pip install flask flask-cors pymongo requests
```

### 2. Instale e Inicie o MongoDB
Baixe: https://www.mongodb.com/try/download/community

Crie a pasta database/ no projeto

Em um terminal separado, rode:
```bash
"C:\Program Files\MongoDB\Server\<versao>\bin\mongod.exe" --dbpath "D:\Documents\FIAP\projeto_microplasticos\database"
```

### 3. Execute o Projeto
No terminal com seu ambiente virtual ativado:
```bash
python main.py
```

### 4. Acesse o Dashboard
Abra o navegador em:

```bash
http://localhost:5000/
```
---

## 📊 Funcionalidades do Dashboard
- Gráfico dinâmico com dados simulados de luminosidade

- **Ponto vermelho**: luminosidade abaixo de 300 → água contaminada

- **Ponto verde**: luminosidade ≥ 300 → água limpa

- Atualização automática a cada 3 segundos

---

## 🧪 Exemplo de Dados no MongoDB
```json
{
  "valor": 243,
  "status": 1,
  "data_hora": "2025-04-11T18:35:12.845Z"
}
```

- valor: valor simulado do sensor de luminosidade

- status: 1 = contaminado | 0 = limpo

- data_hora: registro do momento da leitura

---

## 🧼 Limpeza de Dados
Para apagar todos os registros:
### Pelo Python:
```python
from pymongo import MongoClient
client = MongoClient("localhost", 27017)
client["microplasticos"]["leituras"].delete_many({})
```

### Pelo terminal Mongo:
```bash
mongo
use microplasticos
db.leituras.deleteMany({})
```

---

## 📚 Futuras Evoluções
- Detecção com sensores reais (Arduino + LDR + ESP8266)
- Notificações via app ou e-mail
- Exportação de dados em CSV
- Módulo de alertas
- Dashboard online hospedado (Render, Vercel, etc.)

---

## 👨‍💻 Autores
- Thiago Alves Damascena (RM 355668)
- Marcos Donizeti da Silva (RM 356826)
- Tiago Pessoa de Oliveira (RM 356497)

Projeto desenvolvido para a disciplina de **Robótica e IoT – FIAP (2025)**.

---

## 🧠 ODS Relacionado
ODS 3 – Saúde e Bem-Estar

> Reduzir a exposição a poluentes, como os microplásticos, é um passo importante na promoção de saúde pública.

---

## 📷 Screenshots

[imagem para ser adicionada]