import json
import os
import socket

import grpc
import pika

import controle_pb2
import controle_pb2_grpc


def required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Defina a variável de ambiente {name}")
    return value


MICROSERVICE_HOST = os.getenv("MICROSERVICE_HOST", "127.0.0.1")
MICROSERVICE_PORT = int(os.getenv("MICROSERVICE_PORT", "50051"))
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")
RABBITMQ_USER = required_env("RABBITMQ_USER")
RABBITMQ_PASS = required_env("RABBITMQ_PASS")
SENSOR_UDP_PORT = int(os.getenv("SENSOR_UDP_PORT", "9999"))
ACTUATOR_UDP_HOST = os.getenv("ACTUATOR_UDP_HOST", "127.0.0.1")
ACTUATOR_UDP_PORT = int(os.getenv("ACTUATOR_UDP_PORT", "10000"))

sock_sensor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_sensor.bind(("0.0.0.0", SENSOR_UDP_PORT))
sock_sensor.settimeout(1.0)

channel = grpc.insecure_channel(f"{MICROSERVICE_HOST}:{MICROSERVICE_PORT}")
stub = controle_pb2_grpc.ControladorAmbienteStub(channel)

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
)
channel_rabbit = connection.channel()
channel_rabbit.queue_declare(queue="sensor_data_queue", durable=False)
channel_rabbit.queue_declare(queue="commands_queue", durable=False)

print("Gateway iniciado. Aguardando dados de sensores...")

while True:
    try:
        data, addr = sock_sensor.recvfrom(1024)
    except socket.timeout:
        data = None
    if data:
        mensagem = data.decode()
        try:
            sensor_id_str, valor_str = mensagem.split(":")
            sensor_id = int(sensor_id_str)
            valor = float(valor_str)
        except ValueError:
            print(f"Formato inválido da mensagem recebida: {mensagem}")
            continue

        print(f"[Gateway] Leitura recebida do Sensor {sensor_id}: {valor}")
        sensor_data = controle_pb2.SensorData(id=sensor_id, valor=valor)
        try:
            resposta = stub.ProcessarLeitura(sensor_data)
        except Exception as exc:
            print(f"Erro ao chamar microsserviço gRPC: {exc}")
            resposta = None

        if resposta and resposta.ativar:
            comando_msg = f"{resposta.id}:{resposta.acao}"
            sock_sensor.sendto(
                comando_msg.encode(), (ACTUATOR_UDP_HOST, ACTUATOR_UDP_PORT)
            )
            print(f"[Gateway] Enviando comando para Atuador {resposta.id}: {resposta.acao}")

        dado = {"sensor_id": sensor_id, "valor": valor}
        channel_rabbit.basic_publish(
            exchange="", routing_key="sensor_data_queue", body=json.dumps(dado).encode()
        )

    method_frame, header_frame, body = channel_rabbit.basic_get(
        "commands_queue", auto_ack=True
    )
    if method_frame:
        cmd = body.decode()
        try:
            atuador_id_str, acao = cmd.split(":")
            atuador_id = int(atuador_id_str)
        except ValueError:
            print(f"Comando mal formatado recebido: {cmd}")
            continue
        sock_sensor.sendto(cmd.encode(), (ACTUATOR_UDP_HOST, ACTUATOR_UDP_PORT))
        print(f"[Gateway] Comando manual recebido: Atuador {atuador_id} -> {acao}")
