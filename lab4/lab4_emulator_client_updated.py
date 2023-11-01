# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np


#1: modify the following parameters
#Starting and end index, modify this
device_st = 1
device_end = 10

#Path to the dataset, modify this
data_path = "data2/vehicle{}.csv"

#Path to your certificates, modify this
certificate_formatter = "./certificates/device_{}/device_{}.certificate.pem"
key_formatter = "./certificates/device_{}/device_{}.private.pem"

root_path = "./certificates/root.pem"
endpoint_path = "a2bwa1ru0h9r7v-ats.iot.us-east-2.amazonaws.com"

print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)
    
class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint(endpoint_path, 8883)
        self.client.configureCredentials(root_path, key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, Payload="payload"):
        #4: fill in this function for your publish
        self.client.connect()
        
        id = int(self.device_id)
        if id <= 5:
            self.client.publishAsync("VehicleTopic_CO2", data[id - 1].vehicle_CO2.to_json(orient="values"), 0, ackCallback=self.customPubackCallback)
            self.client.subscribeAsync("VehicleTopic_CO2", 0, ackCallback=self.customSubackCallback)
        
        elif 5 < id < 11:
            self.client.subscribeAsync("VehicleTopic_fuel", 0, ackCallback=self.customSubackCallback)
            self.client.publishAsync("VehicleTopic_fuel", data[id - 6].vehicle_fuel.to_json(orient="values"), 0, ackCallback=self.customPubackCallback)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end + 1):
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    client.client.connect()
    clients.append(client)
 

while True:
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            c.publish()

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)





