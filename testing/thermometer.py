
import PySimpleGUI as sg
import paho.mqtt.client as mqtt

global curTemp
global setTemp

curTempText = "Current Temperature: {}°"
setTempText = "Set Temperature: {}°"
curTemp = 70
setTemp = 70

layout = [[sg.Button("UP", key="up")], [sg.Text(setTempText.format(setTemp), key="setTemp")], [sg.Text(curTempText.format(curTemp), key="curTemp")], [sg.Button("DOWN", key="down")]]

# Create the window
window = sg.Window("Thermometer", layout, element_justification='c')

def on_connect(client, userdata, flags, rc):
    client.subscribe('hah/temperature')

def on_message(client, userdata, msg):
    if msg.topic == 'hah/temperature':
        curTemp = int(msg.payload)
        window['curTemp'].update(curTempText.format(curTemp))
    if msg.topic == 'hah/set_temperature':
        setTemp = int(msg.payload)
        window['setTemp'].update(setTempText.format(setTemp))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)
client.loop_start()

client.publish('hah/temperature', payload=70)
client.publish('hah/set_temperature', payload=70)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
    if event == 'up':
        setTemp = setTemp + 1
        client.publish('hah/set_temperature', payload=setTemp)
        window['setTemp'].update(setTempText.format(setTemp))
    if event == 'down':
        setTemp = setTemp - 1
        client.publish('hah/set_temperature', payload=setTemp)
        window['setTemp'].update(setTempText.format(setTemp))

window.close()