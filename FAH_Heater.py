from telnetlib import Telnet
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType
import paho.mqtt.client as mqtt
import time

TELNET_HOST = "localhost"
TELNET_PORT = 36330

BROKER_HOST = "test.mosquitto.org"
BROKER_PORT = 1883

temp_setting = 72
current_temp = 72
heating = False

def fah_command(command):
    #print("FAH COMMAND: " + str(command))
    FaH_Telnet = Telnet(TELNET_HOST, TELNET_PORT)
    FaH_Telnet.read_until(b"> ")
    FaH_Telnet.write(command.encode('ascii') + b"\n")
    FaH_Telnet.close()

def set_temp(client, userdata, message):
    global temp_setting 
    #print("Set Temp: '" + str(message.payload) + "' on topic '"
    #    + message.topic + "' with QoS " + str(message.qos))
    temp_setting = int(message.payload)
    #print(str(temp_setting))

def update_temp(client, userdata, message):
    global current_temp
    #print("Update Temp: '" + str(message.payload) + "' on topic '"
    #    + message.topic + "' with QoS " + str(message.qos))
    current_temp = int(message.payload)
    #print(str(current_temp))

#def on_message(client, userdata, message):
#    print("Received message '" + str(message.payload) + "' on topic '"
#        + message.topic + "' with QoS " + str(message.qos))

def on_connect(client, userdata, flags, rc):
    print("Connection Status: " + str(rc))
    mclnt.subscribe("hah/#")
    mclnt.message_callback_add("hah/set_temperature", set_temp)
    mclnt.message_callback_add("hah/temperature", update_temp)
    mclnt.publish('hah/heater_state', payload="OFF")
    

mclnt = mqtt.Client(client_id="")
orgbclnt = OpenRGBClient('localhost', 6742, 'Heating at Home Client')
orgbclnt.clear()

#mclnt.on_message = on_message
mclnt.on_connect = on_connect

mclnt.connect(BROKER_HOST, BROKER_PORT)
mclnt.loop_start()


while(True):
    if heating == True:
        print("Heating On. Current Temp: " + str(current_temp) + " Temperature Setting: " + str(temp_setting))
        if current_temp > (temp_setting + 1):
            heating = False
            for device in orgbclnt.devices:
                device.set_color(RGBColor(0,0,255))
                time.sleep(0.05)
            fah_command("pause")
            print("Turning Heating Off")
            mclnt.publish('hah/heater_state', payload="OFF", retain=True)
    else:
        print("Heating Off. Current Temp: " + str(current_temp) + " Temperature Setting: " + str(temp_setting))
        if current_temp < (temp_setting - 1):
            heating = True
            for device in orgbclnt.devices:
                device.set_color(RGBColor(255,0,0))
                time.sleep(0.05)
            fah_command("unpause")
            print("Turning Heating On")
            mclnt.publish('hah/heater_state', payload="ON", retain=True)
    time.sleep(10)


#fah_command("unpause");