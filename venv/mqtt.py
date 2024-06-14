from paho.mqtt import client as mqtt

client_id = "My_connection"
port = 1883
broker = "broker.emqx.io"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
client.connect(broker, port)

client.publish("test", "hello")