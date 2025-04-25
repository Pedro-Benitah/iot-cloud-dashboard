import socket
import grpc
import pika
import controle_pb2
import controle_pb2_grpc
import json

# Configuracoes - substitua pelos IPs reais das instancias correspondentes
MICROSERVICE_HOST = "172.31.92.174"
MICROSERVICE_PORT = 50051
RABBITMQ_HOST    = "172.31.93.110"
RABBITMQ_USER    = "admin"
RABBITMQ_PASS    = "12345."
SENSOR_UDP_PORT  = 9999           # Porta UDP para ouvir sensores
ACTUATOR_UDP_IP  = "172.31.90.54"
ACTUATOR_UDP_PORT= 10000          # Porta UDP dos atuadores

# 1. Preparar socket UDP para ouvir dados de sensores
sock_sensor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_sensor.bind(("0.0.0.0", SENSOR_UDP_PORT))
sock_sensor.settimeout(1.0)  # timeout para nao bloquear indefinidamente

# 2. Conectar ao microsservico gRPC
channel = grpc.insecure_channel(f"{MICROSERVICE_HOST}:{MICROSERVICE_PORT}")
stub = controle_pb2_grpc.ControladorAmbienteStub(channel)

# 3. Conectar ao RabbitMQ (publicar sensor, consumir comandos)
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel_rabbit = connection.channel()
# Declarar filas (idempotente - garante que existem)
channel_rabbit.queue_declare(queue="sensor_data_queue", durable=False)
channel_rabbit.queue_declare(queue="commands_queue", durable=False)

print("Gateway iniciado. Aguardando dados de sensores...")

while True:
    try:
        # 4. Esperar dado de sensor via UDP
        data, addr = sock_sensor.recvfrom(1024)  # pode lancar timeout
    except socket.timeout:
        data = None
    if data:
        mensagem = data.decode()
        # Supondo formato "sensorID:valor"
        try:
            sensor_id_str, valor_str = mensagem.split(":")
            sensor_id = int(sensor_id_str)
            valor = float(valor_str)
        except ValueError:
            print(f"Formato inv\u00e1lido da mensagem recebida: {mensagem}")
            continue

        print(f"[Gateway] Leitura recebida do Sensor {sensor_id}: {valor}")
        # Enviar dados para o microsservico via gRPC
        sensor_data = controle_pb2.SensorData(id=sensor_id, valor=valor)
        try:
            resposta = stub.ProcessarLeitura(sensor_data)   # chamada RPC
        except Exception as e:
            print(f"Erro ao chamar microsservico gRPC: {e}")
            resposta = None

        # Se houve resposta do microsservico, processar comando
        if resposta:
            acao = resposta.acao  # "ON" ou "OFF"
            atuador_id = resposta.id
            if resposta.ativar:
                # Enviar comando via UDP para atuador
                comando_msg = f"{atuador_id}:{acao}"
                sock_sensor.sendto(comando_msg.encode(), (ACTUATOR_UDP_IP, ACTUATOR_UDP_PORT))
                print(f"[Gateway] Enviando comando para Atuador {atuador_id}: {acao}")

        # Publicar a leitura do sensor no RabbitMQ (para o painel web)
        dado = {"sensor_id": sensor_id, "valor": valor}
        channel_rabbit.basic_publish(exchange="", routing_key="sensor_data_queue",
                                     body=json.dumps(dado).encode())
    # 5. Verificar se h\u00e1 comandos manuais pendentes no RabbitMQ
    method_frame, header_frame, body = channel_rabbit.basic_get("commands_queue", auto_ack=True)
    if method_frame:
        # Espera formato "atuadorID:ACAO"
        cmd = body.decode()
        try:
            atuador_id_str, acao = cmd.split(":")
            atuador_id = int(atuador_id_str)
        except ValueError:
            print(f"Comando mal formatado recebido: {cmd}")
            continue
        # Envia comando UDP para atuador
        sock_sensor.sendto(cmd.encode(), (ACTUATOR_UDP_IP, ACTUATOR_UDP_PORT))
        print(f"[Gateway] Comando manual recebido do painel: Atuador {atuador_id} -> {acao}")
