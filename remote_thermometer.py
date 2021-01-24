import asyncio
import argparse
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("hah/temperature")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

parser = argparse.ArgumentParser(description='MQTT thermometer')
parser.add_argument('broker', nargs='?', default='localhost')
parser.add_argument('port', nargs='?', default=1883)
args = parser.parse_args()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(args.broker, port=args.port)
client.loop_start()

while(True):
    # Read from sensor here, if I had one
    client.publish('hah/temperature', payload=60)
    time.sleep(15)
