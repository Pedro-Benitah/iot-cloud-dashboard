# IoT Cloud Dashboard

Protótipo acadêmico de monitoramento de sensores e controle de atuadores em tempo real. O fluxo combina UDP, gRPC, RabbitMQ, Server-Sent Events e uma interface Flask.

## Fluxo

- Sensor -> UDP -> Gateway
- Gateway -> gRPC -> Microsserviço
- Gateway -> RabbitMQ -> Painel web
- Gateway -> UDP -> Atuador
- Painel web -> RabbitMQ -> Gateway

## Tecnologias

Python 3, Flask, gRPC/Protobuf, RabbitMQ, UDP, Server-Sent Events (SSE), HTML, CSS, JavaScript e AWS EC2.

## Componentes

- `sensor.py`: simula leituras e as envia por UDP.
- `gateway.py`: integra UDP, gRPC e RabbitMQ.
- `microsservico.py`: aplica a regra de controle por gRPC.
- `atuador.py`: simula o recebimento de comandos UDP.
- `painel.py`: apresenta leituras por SSE e envia comandos.
- `controle.proto`: contrato do serviço gRPC.

## Configuração

Endpoints e credenciais não ficam no código. Configure-os no ambiente antes de executar:

```bash
export RABBITMQ_HOST=127.0.0.1
export RABBITMQ_USER=SEU_USUARIO
export RABBITMQ_PASS=SUA_SENHA
export MICROSERVICE_HOST=127.0.0.1
export ACTUATOR_UDP_HOST=127.0.0.1
export GATEWAY_UDP_HOST=127.0.0.1
```

Há variáveis opcionais para as portas: `MICROSERVICE_PORT`, `SENSOR_UDP_PORT`, `ACTUATOR_UDP_PORT`, `GATEWAY_UDP_PORT` e `WEB_PORT`. O painel usa `127.0.0.1` por padrão; defina `WEB_HOST` conscientemente se precisar expô-lo.

Nunca use credenciais reais em commits. Se credenciais anteriormente publicadas ainda estiverem ativas, rotacione-as no RabbitMQ e no provedor de nuvem.

## Execução local

Com RabbitMQ disponível e as variáveis configuradas, abra terminais separados:

```bash
python3 microsservico.py
python3 atuador.py
python3 gateway.py
python3 painel.py
python3 sensor.py 1
```

Acesse `http://127.0.0.1:5000` para visualizar o painel.

## Validação e limitações

O projeto demonstra o fluxo ponta a ponta entre componentes. Ainda não há suíte automatizada, cobertura medida, autenticação da interface, TLS ou garantias de produção. O caminho de comandos manuais permanece um protótipo e deve ser testado e endurecido antes de qualquer uso real.

## Escopo

Projeto educacional desenvolvido em 2025. Não representa um produto de produção nem contém dados de clientes.
