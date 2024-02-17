import socket
import configparser


def listening():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)