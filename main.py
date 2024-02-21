import mcu_server
import frontend_server
import threading


if __name__ == '__main__':
    t_muc_listening = threading.Thread(target=mcu_server.listening)
    t_frontend_listening = threading.Thread(target=frontend_server.listening)
    t_muc_listening.start()
    t_frontend_listening.start()
