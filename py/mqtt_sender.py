import paho.mqtt.client as mqtt
import json
import time


class MQTTSender:
    """
    Класс для отправки команд через MQTT брокер Mosquitto
    Использование:
        sender = MQTTSender(broker_host="localhost", broker_port=1883)
        sender.send({"comman": "forward", "id": 1, "time": 1.0})
    """

    def __init__(self, broker_host="localhost", broker_port=1883, topic="robot/commands"):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic
        self.client = mqtt.Client()
        self.connected = False

        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

        self.connect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT broker at {self.broker_host}:{self.broker_port}")
            self.connected = True
        else:
            print(f"Failed to connect to MQTT broker, error code: {rc}")
            self.connected = False

    def on_publish(self, client, userdata, mid):
        print(f"Command sent via MQTT, message ID: {mid}")

    def connect(self):
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            time.sleep(0.5)
        except Exception as e:
            print(f"MQTT connection error: {e}")
            self.connected = False

    def send(self, command):
        """Отправка команды через MQTT"""
        if not self.connected:
            print("Not connected to MQTT broker, command not sent")
            return False

        payload = json.dumps(command, ensure_ascii=False)
        result = self.client.publish(self.topic, payload, qos=1)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Command published: {payload}")
            return True
        else:
            print(f"Publish failed, error code: {result.rc}")
            return False

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT broker")


# Пример запуска отдельно для тестирования
if __name__ == "__main__":
    # Тестовая команда
    data = {
        "comman": "forward",
        "id": 33,
        "time": 1.00
    }

    sender = MQTTSender()
    sender.send(data)
    time.sleep(1)
    sender.disconnect()