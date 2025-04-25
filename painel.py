from flask import Flask, render_template_string, Response, request
import pika, threading, queue, json

# Configuração do RabbitMQ
RABBITMQ_HOST = "52.70.149.95"
RABBITMQ_USER = "admin"
RABBITMQ_PASS = "12345."

app = Flask(__name__)

# Dados globais
sensor_values = {}
data_queue = queue.Queue()
actuators = [
    {"id": "ac", "name": "Ar-condicionado"},
    {"id": "light", "name": "Iluminação"},
    {"id": "alarm", "name": "Alarme"}
]

# Thread do consumidor RabbitMQ
def consume_sensor_data():
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue="sensor_data_queue", durable=False)

        def callback(ch, method, properties, body):
            try:
                data = json.loads(body.decode())
                sensor_id = str(data.get("sensor_id") or data.get("sensor") or data.get("id"))
                valor = data.get("valor") or data.get("value")
                if sensor_id and valor is not None:
                    sensor_values[sensor_id] = valor
                    data_queue.put(json.dumps({sensor_id: valor}))
                    print(f"[Painel] Sensor atualizado: {sensor_id} = {valor}")
            except Exception as e:
                print("Erro ao processar mensagem:", e)

        channel.basic_consume(queue="sensor_data_queue", on_message_callback=callback, auto_ack=True)
        print("[Painel] Consumindo dados da fila sensor_data_queue...")
        channel.start_consuming()
    except Exception as e:
        print("Erro ao conectar no RabbitMQ:", e)

# Rotas
@app.route('/')
def index():
    return render_template_string(TEMPLATE, sensors=sensor_values, actuators=actuators)

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            data = data_queue.get()
            yield f"data: {data}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/actuator/<act_id>/<action>', methods=["POST"])
def send_command(act_id, action):
    try:
        cmd = json.dumps({"actuator": act_id, "action": action})
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue="commands_queue", durable=False)
        channel.basic_publish(exchange="", routing_key="commands_queue", body=cmd)
        print(f"[Painel] Comando enviado: {cmd}")
        connection.close()
        return "OK"
    except Exception as e:
        print("Erro ao enviar comando:", e)
        return "Erro", 500

# HTML + CSS + JavaScript
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Painel de Monitoramento</title>
    <style>
        body { font-family: Arial; background: #f2f2f2; padding: 20px; }
        h1 { text-align: center; }
        .container { display: flex; justify-content: center; gap: 40px; margin-top: 30px; }
        .box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px #ccc; width: 400px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 8px; text-align: center; border-bottom: 1px solid #ddd; }
        button { padding: 6px 12px; margin: 5px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <h1>Painel de Controle</h1>
    <div class="container">
        <div class="box">
            <h2>Sensores</h2>
            <table>
                <tr><th>ID</th><th>Valor</th></tr>
                {% for sid, val in sensors.items() %}
                <tr><td>{{ sid }}</td><td id="sensor-{{ sid }}">{{ val }}</td></tr>
                {% else %}
                <tr><td colspan="2">Nenhum dado ainda</td></tr>
                {% endfor %}
            </table>
        </div>
        <div class="box">
            <h2>Atuadores</h2>
            {% for act in actuators %}
            <div><b>{{ act.name }}</b><br>
                <button onclick="sendCommand('{{ act.id }}', 'on')">Ligar</button>
                <button onclick="sendCommand('{{ act.id }}', 'off')">Desligar</button>
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
        const evtSource = new EventSource("/stream");
        evtSource.onmessage = function(e) {
            const data = JSON.parse(e.data);
            for (const [id, val] of Object.entries(data)) {
                const el = document.getElementById("sensor-" + id);
                if (el) el.textContent = val;
            }
        };

        function sendCommand(actuator, action) {
            fetch(`/actuator/${actuator}/${action}`, { method: "POST" })
            .then(res => {
                if (!res.ok) alert("Erro ao enviar comando.");
            });
        }
    </script>
</body>
</html>
"""

# Iniciar aplicação e thread
if __name__ == "__main__":
    threading.Thread(target=consume_sensor_data, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
