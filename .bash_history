ls
nano controle.proto
sudo apt-get install -y python3-pip        # caso pip n\u00e3o esteja instalado
pip3 install grpcio grpcio-tools          # instala gRPC runtime e protoc plugin
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. controle.proto
sudo apt update
sudo add-apt-repository universe
sudo apt update
sudo apt install -y software-properties-common
sudo apt install -y python3-pip
sudo apt install -y python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install grpcio grpcio-tools
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. controle.proto
ls
nano microsservico.py
python3 microsservico.py
nano microsservico.py
python3 microsservico.py
