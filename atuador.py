import socket

LISTEN_PORT = 10000  # Porta UDP para ouvir comandos do Gateway

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", LISTEN_PORT))
print(f"Atuador(simulado) escutando comandos na porta {LISTEN_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    if not data:
        continue
    mensagem = data.decode()
    try:
        atuador_id, acao = mensagem.split(":")
    except ValueError:
        print(f"Comando inv\u00e1lido recebido: {mensagem}")
        continue
    print(f"[Atuador {atuador_id}] Comando recebido: {acao}")
    # Aqui poder\u00edamos implementar a l\u00f3gica do atuador, e.g., ligar/desligar algo.
