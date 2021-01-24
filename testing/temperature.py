import paho.mqtt.client as mqtt
import time

curTemp = 70
heaterState = "ON"

def on_connect(client, userdata, flags, rc):
    
    print("Connected with result code "+str(rc))
    client.subscribe('hah/temperature')
    client.subscribe('hah/heater_state')

def on_message(client, userdata, msg):
    global curTemp
    global heaterState
    if msg.topic == 'hah/temperature':
        curTemp = int(msg.payload)
    if msg.topic == 'hah/heater_state':
        heaterState = msg.payload.decode("utf-8")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)
client.loop_start()

client.publish('hah/temperature', payload=70)

while True:
    if heaterState == "ON":
        curTemp = curTemp + 1
    else:
        curTemp = curTemp - 1
    client.publish('hah/temperature', payload=curTemp)
    time.sleep(8)