import configparser
import socket
import threading
import main


config = configparser.ConfigParser()
config.read('config.ini')
socket_threading_num = 0


def listening():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = config.get('frontend_server', 'host')
    port = int(config.get('frontend_server', 'port'))
    server_socket.bind((host, port))
    server_socket.listen(0)
    print('开始侦听前端')
    while True:
        client_socket, addr = server_socket.accept()
        if client_socket:
            print("来自{}:{}的连接".format(addr[0], addr[1]))
            main.c_main_socket_list.append(client_socket)
            t = threading.Thread(target=main.socket_threading, args=(0, client_socket), name="P" + str(addr[1]))
            t.start()
        print("已添加连接进程，开始监听新连接")


def t_frontend(c_socket):
    print(c_socket)
