import configparser
import socket
import sql

config = configparser.ConfigParser()
config.read('config.ini')


def listening():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = config.get('mcu_server', 'host')
    port = int(config.get('mcu_server', 'port'))
    server_socket.bind((host, port))
    server_socket.listen(0)
    print('开始侦听单片机\n')
    while True:
        client_socket, addr = server_socket.accept()
        print("来自{}:{}的连接".format(addr[0], addr[1]))
        data = client_socket.recv(128).decode()
        sql.data_processing(data)
