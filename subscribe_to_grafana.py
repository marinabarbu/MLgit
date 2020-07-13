import paho.mqtt.client as mqtt
import re
import numpy as np
import paho.mqtt.publish as publish
import torch
import json

#topic = 'meshliumfa30/WINSHI/#'
topic = 'meshliumfa30/SCP3/PM10/#'
# topic = 'meshliumfa30/Metrorex/PM10'
topic_for_publish = 'meshliumfa30/SCP3/PP10'
topic_for_publish_mean_value = 'meshliumfa30/SCP3/PMA10'
MQTT_server = "mqtt.beia-telemetrie.ro"
MQTT_port = 1883

lista_ore = []

# value = 60.0
# payload = json.dumps({'predicted': value})
# publish.single(topic_for_publish, payload=payload, hostname=MQTT_server, port=MQTT_port)



# functie public pentru trimiterea datelor prezise pe grafana
# media reala -> diferenta intre prezis si real
# descrierea metodei -> ro





clf = torch.load("model_large_dataset")

def on_connect(client, userdata, flags, rc):
    # print("Connect with Code: ", str(rc))
    #Subscribe Topic:
    client.subscribe(topic)

preds = []

def on_message(client, userdata, msg):
    predicted = 0
    m = str(msg.payload)
    print(m)
    text = re.findall('"([^"]*)"', m) #selectarea string-urilor dintre ghilimele
    value = float(text[9])
    timestamp = text[11]
    hour = float(timestamp[11:13])
    print("value: ", value)
    print("Timestamp: ", timestamp)
    print("Hour: ", hour)

    if len(lista_ore) > 0:
        if lista_ore[-1][0] == hour:
            lista_ore.append([hour, np.float64(round(value))])
            print(lista_ore)
            print(hour, np.float64(round(value)), (hour + 1)%24)
        else:
            print("Aici!")
            l = []
            medie = np.mean([x[1] for x in lista_ore])
            print("Real mean value for ", lista_ore[-1][0], " hour is ", medie)
            print([lista_ore[-1][0], medie, hour])
            print([lista_ore[-1][0], float(round(medie)), hour])
            l.append(lista_ore[-1][0])
            l.append(float(round(medie)))
            l.append(hour)
            payload = json.dumps({'mean': medie})
            publish.single(topic_for_publish_mean_value, payload=payload, hostname=MQTT_server, port=MQTT_port)

            if len(preds) > 0:
                print(preds)
                print(preds[-1])
                p = preds[-1]
                payload = json.dumps({'predicted': p})
                publish.single(topic_for_publish, payload=payload, hostname=MQTT_server, port=MQTT_port)

            predicted = clf.predict([l])
            print("Predicted mean value for ", hour, " hour: ", predicted[0])
            print("predicted list: ", preds)
            preds.append(predicted[0])
            lista_ore.clear()
            lista_ore.append([hour, round(value)])
            print(lista_ore)
    else:
        lista_ore.append([hour, round(value)])
        l = []
        l.append(hour)
        l.append(round(value))
        l.append((hour + 1)%24)
        l[1] = np.float64(l[1])
        print(l)
        predicted = clf.predict([l])
        print("Predicted: ", predicted[0])


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.beia-telemetrie.ro", 1883, 60)
client.loop_forever()