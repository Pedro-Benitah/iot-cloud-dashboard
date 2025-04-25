import grpc
from concurrent import futures
import controle_pb2
import controle_pb2_grpc

# Definindo a classe do servico com a implementacao do RPC
class ControladorAmbienteServicer(controle_pb2_grpc.ControladorAmbienteServicer):
    def ProcessarLeitura(self, request, context):
        sensor_id = request.id
        valor = request.valor
        # L\u00f3gica simples: se valor > 30.0, liga o atuador; caso contr\u00e1rio, desliga
        comando = controle_pb2.ActuatorCommand()
        comando.id = sensor_id            # supondo atuador com mesmo ID do sensor
        if valor > 30.0:
            comando.acao = "ON"
            comando.ativar = True
        else:
            comando.acao = "OFF"
            comando.ativar = False
        print(f"[Microsservi\u00e7o] Sensor {sensor_id} valor={valor:.2f} => acao='{comando.acao}'")
        return comando

def iniciar_servidor():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    controle_pb2_grpc.add_ControladorAmbienteServicer_to_server(ControladorAmbienteServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Microsservi\u00e7o gRPC escutando na porta 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    iniciar_servidor()
