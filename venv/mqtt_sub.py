from paho.mqtt import client as mqtt
import time


broker = 'broker.emqx.io'
port = 1883
client_id = 'My_connection'

mac = '00-50-B6-5B-CA-6A'
topic = 'DEVICES/'+mac+'/INFO/'

class State:
    def __init__(self, state):
        self.state = state

state_msg = State(False)

class Message:
    def __init__(self, topic, text):
        self.topic = topic
        self.text = text

msg_user = Message('','')

def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Подключено к MQTT Брокеру")
        else:
            print("Подключение не установлено, %d\n", rc)

    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        if msg.topic == topic:
            state_msg.state = True

        msg_user.text = msg.payload.decode()
        msg_user.topic = msg.topic

    client.subscribe(topic)
    client.on_message = on_message

def mqtt_run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()

def mqtt_stop():
    client.disconnect()
    client.loop_stop()