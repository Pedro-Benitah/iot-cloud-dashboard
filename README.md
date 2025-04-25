
# IoT Cloud Dashboard

Este projeto implementa um sistema completo de monitoramento de sensores e controle de atuadores em tempo real, com visualização web, utilizando Python, gRPC, Flask e RabbitMQ em instâncias EC2 da AWS.

## 📌 Componentes

### 1. `sensor.py`
Simula sensores físicos. Envia dados via UDP para o Gateway.
- Exemplo: `python3 sensor.py 1` enviará dados como `1:35.2`

### 2. `gateway.py`
Recebe dados dos sensores via UDP, envia para o microsserviço via gRPC, e transmite comandos aos atuadores via UDP. Também publica dados no RabbitMQ para consumo pelo painel.

### 3. `microsservico.py`
Um microsserviço gRPC que processa os dados dos sensores e decide ações simples:
- Se valor > 30 → retorna comando `ON`
- Caso contrário → retorna `OFF`

### 4. `atuador.py`
Simula um dispositivo atuador escutando comandos via UDP. Ao receber um comando como `1:ON`, imprime a ação.

### 5. `painel.py`
Interface web feita com Flask, HTML, CSS e JavaScript.
- Visualiza valores dos sensores em tempo real usando SSE.
- Envia comandos de controle para os atuadores via RabbitMQ.

## 🛰️ Comunicação

- Sensores → UDP → Gateway
- Gateway → gRPC → Microsserviço
- Gateway → UDP → Atuadores
- Gateway ↔ RabbitMQ ↔ Painel Web

## 📦 Tecnologias

- Python 3.10+
- Flask
- gRPC
- RabbitMQ
- Socket UDP
- Server-Sent Events (SSE)
- AWS EC2

## 📁 Arquivos do projeto

| Arquivo                 | Descrição                                           |
|------------------------|-----------------------------------------------------|
| `sensor.py`            | Simulador de sensores UDP                           |
| `atuador.py`           | Simulador de atuadores UDP                          |
| `gateway.py`           | Orquestrador UDP/gRPC/RabbitMQ                      |
| `microsservico.py`     | Microsserviço gRPC com lógica de controle           |
| `painel.py`            | Painel de controle e visualização em Flask          |
| `controle.proto`       | Definição do serviço gRPC                           |
| `controle_pb2.py`      | Arquivo gerado do proto (mensagens)                 |
| `controle_pb2_grpc.py` | Arquivo gerado do proto (serviço)                   |

## 🚀 Como rodar o projeto

1. Configure o RabbitMQ (ex: via Docker ou EC2)
2. Rode os serviços em diferentes terminais ou instâncias:
    ```bash
    python3 microsservico.py
    python3 gateway.py
    python3 painel.py
    python3 atuador.py
    python3 sensor.py 1
    python3 sensor.py 2
    ```

3. Acesse o painel via navegador:
    ```
    http://<IP-DA-EC2>:5000
    ```

---

Desenvolvido por Pedro Benitah — 2025
