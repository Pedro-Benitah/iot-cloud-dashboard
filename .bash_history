sudo apt-get update
sudo apt-get install -y rabbitmq-server
sudo apt-get update
sudo apt-get install -y rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management
sudo systemctl restart rabbitmq-server
sudo systemctl status rabbitmq-server
sudo rabbitmqctl add_user admin 12345.
sudo rabbitmqctl set_user_tags admin administrator
sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
telnet 52.90.12.112 8672
telnet 52.90.12.112 5672
nano controle.proto
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. controle.proto
sudo apt-get install -y python3-pip        # caso pip n\u00e3o esteja instalado
pip3 install grpcio grpcio-tools          # instala gRPC runtime e protoc plugin
sudo apt-get install -y python3-pip        # caso pip n\u00e3o esteja instalado
pip3 install grpcio grpcio-tools          # instala gRPC runtime e protoc plugin
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. controle.proto
python3 -m venv venv
source venv/bin/activate
pip install grpcio grpcio-tools
python3 -m venv venv
apt install python3.12-venv
source venv/bin/activate
python3 -m venv venv
source venv/bin/activate
pip install grpcio grpcio-tools
sudo apt install -y python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. controle.proto
ls
nano microsservico.py
python3 microsservico.py
telnet 52.90.12.112 5672
sudo systemctl status rabbitmq-server
sudo systemctl restart rabbitmq-server
sudo systemctl status rabbitmq-server
telnet 52.90.12.112 5672
sudo tail -n 50 /var/log/rabbitmq/rabbit@*.log
sudo rabbitmqctl list_users
sudo rabbitmqctl list_permissions -p /
sudo systemctl restart rabbitmq-server
telnet 52.90.12.112 5672
sudo rabbitmqctl list_connections
telnet 52.90.12.112 5672
