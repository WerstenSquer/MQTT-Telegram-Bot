from paho.mqtt import client as mqtt
import json

broker = 'broker.emqx.io'
port = 1883
client_id = 'My_connection'

mac = '00-50-B6-5B-CA-6A'
mac2 = '00-50-B6-5B-DB-5B'

topic_all = 'DEVICES/#'

class Info:
    def __init__(self, topic, text):
        self.topic = topic
        self.text = text

msg_info = Info('','')
dict_msg_info = {}
client = ''

def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Подключено к MQTT Брокеру")
        else:
            print("Подключение не установлено, %d\n", rc)
    global client
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt, topic_list):
    def on_message(client, userdata, msg):
        topic = msg.topic
        json_msg = json.loads(msg.payload.decode())

        list_param = []
        for key, value in json_msg.items():
            list_param.append("{0}: {1}".format(key,value))

        msg_info.topic = topic
        msg_info.text = list_param
        dict_msg_info.update({topic: list_param})

    for topic_mac in topic_list:
        client.subscribe(topic_mac)
    client.on_message = on_message

def update(topic_list):
    for topic_mac in topic_list:
        client.subscribe(topic_mac)

def unsubscribe(topic):
    client.unsubscribe(topic)

def mqtt_run(topic_list):
    client = connect_mqtt()
    subscribe(client, topic_list)
    client.loop_start()

def mqtt_stop():
    client.disconnect()
    client.loop_stop()