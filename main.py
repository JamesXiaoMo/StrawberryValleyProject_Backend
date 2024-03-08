import time
import mcu_server
import frontend_server
import threading

import sql

c_main_socket_list = []
c_fd_socket_list = []
interrupt = 0


def socket_threading(socket_type: int, c_socket):
    if socket_type == 0:
        while True:
            try:
                data = c_socket.recv(1024).decode('utf-8')
                if data == 'connect':
                    s_print("连接成功")
                elif data == "hour":
                    print("尝试数据库获取一小时的数据")
                    sql.sql_search_data("hour")
                    time.sleep(1)
                    with open("hour.json", 'rb') as f:
                        while True:
                            f_data = f.read(1024)
                            c_socket.sendall(f_data)
                            if not f_data:
                                break
                    time.sleep(1)
                    c_socket.send("end".encode('utf-8'))
                    print('ok')
                elif data == "day":
                    print("尝试数据库获取一天的数据")
                    sql.sql_search_data("day")
                    time.sleep(1)
                    with open("day.json", 'rb') as f:
                        while True:
                            f_data = f.read(1024)
                            c_socket.sendall(f_data)
                            if not f_data:
                                break
                    time.sleep(1)
                    c_socket.send("end".encode('utf-8'))
                    print('ok')
                elif data == "week":
                    print("尝试数据库获取一周的数据")
                    sql.sql_search_data("week")
                    time.sleep(1)
                    with open("week.json", 'rb') as f:
                        while True:
                            f_data = f.read(1024)
                            c_socket.sendall(f_data)
                            if not f_data:
                                break
                    time.sleep(1)
                    c_socket.send("end".encode('utf-8'))
                    print('ok')
                elif data == "month":
                    print("尝试数据库获取一月的数据")
                    sql.sql_search_data("month")
                    time.sleep(1)
                    with open("month.json", 'rb') as f:
                        while True:
                            f_data = f.read(1024)
                            c_socket.sendall(f_data)
                            if not f_data:
                                break
                    time.sleep(1)
                    c_socket.send("end".encode('utf-8'))
                    print('ok')
                elif data == "year":
                    print("尝试数据库获取一年的数据")
                    sql.sql_search_data("year")
                    time.sleep(1)
                    with open("year.json", 'rb') as f:
                        while True:
                            f_data = f.read(1024)
                            c_socket.sendall(f_data)
                            if not f_data:
                                break
                    time.sleep(1)
                    c_socket.send("end".encode('utf-8'))
                    print('ok')
            except ConnectionAbortedError as e:
                c_main_socket_list.remove(c_socket)
                print("客户端连接断开")
                print(c_main_socket_list)
                break
            except ConnectionResetError as e:
                c_main_socket_list.remove(c_socket)
                print("远程主机强迫关闭了一个现有的连接")
                print(c_main_socket_list)
                break


def s_print(msg: str):
    global interrupt
    if len(c_main_socket_list) != 0:
        if interrupt == 0:
            interrupt = 1
            c_main_socket_list[0].send(msg.encode('utf-8'))
            interrupt = 0


if __name__ == '__main__':
    t_muc_listening = threading.Thread(target=mcu_server.listening)
    t_frontend_listening = threading.Thread(target=frontend_server.listening)
    t_muc_listening.start()
    t_frontend_listening.start()
    t_muc_listening.join()
    t_frontend_listening.join()
