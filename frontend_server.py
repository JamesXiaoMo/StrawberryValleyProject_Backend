import configparser
import socket


config = configparser.ConfigParser()
config.read('config.ini')


def listening():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = config.get('frontend_server', 'host')
    port = int(config.get('frontend_server', 'port'))
    server_socket.bind((host, port))
    server_socket.listen(0)
    print('开始侦听前端\n')
    while True:
        client_socket, addr = server_socket.accept()
        print("来自{}:{}的连接".format(addr[0], addr[1]))
        data = client_socket.recv(128).decode()
        if data == 'login':
            client_socket.send('login_ok'.encode('utf-8'))