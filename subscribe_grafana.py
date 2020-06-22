import paho.mqtt.client as mqtt
import re

#topic = 'meshliumfa30/WINSHI/#'
#topic = 'odsi/raspberry/marina_barbu'
topic = 'meshliumfa30/SCP3/PM10/#'
# topic = 'meshliumfa30/Metrorex/PM10'

hours = [0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12., 13., 14., 15., 16., 17., 18., 19., 20., 21., 22., 23.]
lista_ore = []
import torch

clf = torch.load("model_large_dataset")

def on_connect(client, userdata, flags, rc):
    # print("Connect with Code: ", str(rc))
    #Subscribe Topic:
    client.subscribe(topic)

def on_message(client, userdata, msg):
    m = str(msg.payload)
    print(m)
    text = re.findall('"([^"]*)"', m) #selectarea string-urilor dintre ghilimele
    # print(text)
    value = text[9]
    timestamp = text[11]
    hour = timestamp[11:13]
    print("value: ", value)
    print("Timestamp: ", timestamp)
    print("Hour: ", hour)

    if len(lista_ore) > 0:
        if lista_ore[-1][0] == hour:
            lista_ore.append([hour, float(round(value))])
            print(lista_ore)
        else:
            mean = sum([x[1] for x in lista_ore])/len(lista_ore)
            print([float(lista_ore[-1][0]), float(round(mean)), float(hour)])
            predict = clf.predict([float(lista_ore[-1][0]), float(round(mean)), float(hour)])
            print(predict)
            lista_ore.clear()
            lista_ore.append([hour, float(round(value))])
            print(lista_ore)
    else:
        lista_ore.append([hour, float(round(value))])
        print(lista_ore)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.beia-telemetrie.ro", 1883, 60)
client.loop_forever()