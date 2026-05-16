"""
Запускает QR сканер с отправкой команд через MQTT
"""
from qr_scanner import AppServ
from mqtt_sender import MQTTSender

if __name__ == "__main__":
    # Настройки MQTT брокера
    BROKER_HOST = "localhost"  # Или IP вашего брокера
    BROKER_PORT = 1883
    TOPIC = "robot/commands"

    sender = MQTTSender(
        broker_host=BROKER_HOST,
        broker_port=BROKER_PORT,
        topic=TOPIC
    )
    app = AppServ(sender=sender)
    app.run()

    # Отключаемся после завершения
    sender.disconnect()