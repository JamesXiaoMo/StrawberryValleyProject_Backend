import mcu_server
import threading


t = threading.Thread(target=tcp_server.listening())
t.start()
t.join()
