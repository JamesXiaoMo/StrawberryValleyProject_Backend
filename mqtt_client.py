import random
import time
import configparser
from paho.mqtt import client as mqtt_client

config = configparser.ConfigParser()
config.read('config.ini')

server_addr = config.get('mqtt', 'server_addr')
port = config.get('mqtt', 'port')
topic = config.get('mqtt', 'topic')
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT server")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(server_addr, port)
    return client


def publish(client, msg):
    time.sleep(1)
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
