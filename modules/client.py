############################################
#auteur : Alberto Oviedo
#fichier: client.py
#date : 18 mai 2022
#description: classe clientmqtt qui permet la reception en envoie de topics
############################################

import json
import sys
import signal
import paho.mqtt.client as mqtt

class MQTTClient:
    __brokerHost = "localhost"  # curl ifconfig.me to get public ip address
    __brokerPort = 1884
    __idClient = "client1"
    __client = None`
    __topicSystem = "system"
    __topicSensor = "sensor"   
    __topicTemp = "sensor/temperature"
    __topicMouvement = "sensor/mouvement"
    __topicWaterLevel = "sensor/waterLevel"
    __system = None
    __tempEau= None

    # init du client mqtt
    def __init__(self, brokerHost, brokerPort, idClient, topicSystem, topicMouvement, topicTemperature,topicWaterLevel):
        self.__brokerHost = brokerHost
        self.__brokerPort = brokerPort
        self.__idClient = idClient
        self.__topicSystem = topicSystem
        self.__topicTemp = topicTemperature
        self.__topicMouvement = topicMouvement
        self.__topicWaterLevel = topicWaterLevel
        self.init_mqtt()

    # brokerHost
    def set_brokerHost(self, host):
        self.__brokerHost = host

    def get_brokerHost(self):
        return self.__brokerHost

    brokerHost = property(get_brokerHost, set_brokerHost)
    # brokerPort
    def set_brokerPort(self, port):
        self.__brokerPort = port

    def get_brokerPort(self):
        return self.__brokerPort

    brokerPort = property(get_brokerPort, set_brokerPort)

    # idClient
    def set_idClient(self, id):
        self.__idClient = id

    def get_idClient(self):
        return self.__idClient

    idClient = property(get_idClient, set_idClient)


    # client
    def set_client(self, client):
        self.__client = client

    def get_client(self):
        return self.__client

    client = property(get_client, set_client)

    # topicSystem
    def set_topicSystem(self, topicSystem):
        self.__topicSystem = topicSystem

    def get_topicSystem(self):
        return self.__topicSystem

    topicSystem = property(get_topicSystem, set_topicSystem)


    # topicTemperature
    def set_topicTemperature(self, topicTemperature):
        self.__topicTemp = topicTemperature

    def get_topicTemperature(self):
        return self.__topicTemp
    topicTemp = property(get_topicTemperature, set_topicTemperature)

    def set_topicMouvement(self, topicMouvement):
        self.__topicMouvement    = topicMouvement

    def get_topicMouvement(self):
        return self.__topicMouvement 
    
    topicMouvement = property(get_topicMouvement, set_topicMouvement)

    def get_topicWaterLevel(self):
        return self.__topicWaterLevel
    def set_topicWaterLevel(self, topicWaterLevel)
        self.__topicWaterLevel = topicWaterLevel

    
    topicWaterLEvel = property(get_topicWaterLevel, set_topicWaterLevel)

    def on_connect(self, client, user_data, flags, connection_result_code):
        if connection_result_code == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect to MQTT Broker: " + mqtt.connack_string(connection_result_code))
            #subscripbe aux topics
        self.client.subscribe(self.topicSystem, qos=2)
        self.client.subscribe(self.topicTemperature, qos=2)


    # when the client disconnects, do this
    def on_disconnect(self, client, user_data, disconnection_result_code):
        print("Disconnected from MQTT broker")

    # when the client receives a message, do this
    def on_message(self, client, user_data, msg):
        data = None
        try:
            data = json.loads(msg.payload.decode("UTF-8"))
        except json.JSONDecodeError as e:
            print("JSON Decode Error: " + msg.payload.decode("UTF-8"))

        if(self.idClient == "client1"): 
            print("Received message for topic {}: {}".format( msg.topic, msg.payload))
            if msg.topic == self.topicSystem:
                print("Circuit")
            elif msg.topic == self.topicTemperature:
                print("Température")
            else:
                print("Unhandled message topic {} with payload " + str(msg.topic, msg.payload))

        elif(self.idClient == "waterPump"):
            if msg.topic == self.topicSystem:
                if data['system'] == 'TURNON':
                    self.system = True
                elif data['system'] == 'SHUTDOWN':
                    self.system = False
            if msg.tpic == self.topicMouvement
                self.__tempEau= Int(data['niveau'])
                print("niveau called")

    def signal_handler(self, sig, frame):
        print("You pressed Control + C. Shutting down, please wait...")
        self.client.disconnect()
        sys.exit(0)

    # init mqtt for usage
    def init_mqtt(self):
        global client
        self.client = mqtt.Client(
            client_id = self.idClient,
            clean_session = False
        )

        # Route Paho logging to Python logging.
        # client.enable_logger()

        # Setup callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        # Connect to Broker.
        self.client.connect(self.brokerHost, self.brokerPort)

    # begins to listen or to send messages
    def startMQTT(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        print("Listening for messages on topic '" + self.topicSystem + "'. Press Control + C to exit.")
        self.client.loop_start()
        signal.pause()

    # stops listening or sending messages
    def stopMQTT(self):
        self.client.loop_stop()
        self.client.disconnect()

    # Publishes a message
    def publish(self, topic, msg):
        self.client.publish(topic,json.dumps(msg),1)

