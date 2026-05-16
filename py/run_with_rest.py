"""
Запускает QR сканер с отправкой команд через REST API
"""

from qr_scanner import AppServ
from rest_sender import RESTSender

if __name__ == "__main__":
    # Укажите URL вашего REST сервера на роботе
    ROBOT_URL = "http://localhost:8000/commands"  # Замените на IP робота

    sender = RESTSender(url=ROBOT_URL)
    app = AppServ(sender=sender)
    app.run()