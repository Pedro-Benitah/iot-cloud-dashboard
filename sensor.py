import socket, time, random, sys

GATEWAY_IP   = "172.31.94.16"
GATEWAY_PORT = 9999  # Porta UDP do Gateway

# Permitir definir um ID do sensor via argumento de linha de comando
sensor_id = 1
if len(sys.argv) > 1:
    sensor_id = int(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Sensor {sensor_id} iniciado, enviando dados para {GATEWAY_IP}:{GATEWAY_PORT}...")
while True:
    # Gerar um valor de sensor aleat\u00f3rio (ex: temperatura entre 20 e 40)
    valor = random.uniform(20.0, 40.0)
    mensagem = f"{sensor_id}:{valor:.2f}"
    sock.sendto(mensagem.encode(), (GATEWAY_IP, GATEWAY_PORT))
    print(f"[Sensor {sensor_id}] Enviou leitura: {mensagem}")
    time.sleep(5)  # esperar 5 segundos at\u00e9 a pr\u00f3xima leitura
