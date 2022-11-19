from paho.mqtt import client as mqtt_client


class MQTT():
    def __init__(self) -> None:
        self.broker = 'broker.emqx.io'
        self.port = 1883
        self.topic = "ICOMP_IOT_MONITORING"
        # generate client ID with pub prefix randomly
        self.client_id = f'python-mqtt-{0}'
        self.username = 'emqx'
        self.password = 'public'
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client = mqtt_client.Client(self.client_id)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
    def publish(self, msg):
        aux =True
        while(aux):
            result = self.client.publish(self.topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{self.topic}`")
                aux = False
            else:
                print(f"Failed to send message to topic {self.topic}")
    def setup(self):
        self.connect_mqtt()
        self.client.loop_start()
