import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.connect(('192.168.0.101', 9213))
s.sendall("wifi".encode('utf-8'))
s.close()