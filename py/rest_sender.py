import requests
import json

class RESTSender:
    """
    Класс для отправки команд через REST API
    Использование:
        sender = RESTSender(url="http://localhost:8080/commands")
        sender.send({"comman": "forward", "id": 1, "time": 1.0})
    """

    def __init__(self, url="http://localhost:8080/commands"):
        self.url = url

    def send_post(self, command):
        """Отправка команды через POST запрос"""
        try:
            response = requests.post(self.url, json=command, timeout=5)
            if response.status_code == 200:
                print("Request successful!")
                print("Response JSON:", response.json())
                return True
            else:
                print(f"Request failed with status code {response.status_code}")
                print("Response text:", response.text)
                return False
        except requests.exceptions.ConnectionError:
            print(f"Connection error: Cannot reach {self.url}")
            return False
        except Exception as e:
            print(f"Error sending command: {e}")
            return False

    def send_get(self, command):
        """Отправка команды через GET запрос"""
        try:
            response = requests.get(self.url, json=command, timeout=5)
            if response.status_code == 200:
                print("GET request successful!")
                return True
            else:
                print(f"GET request failed with status code {response.status_code}")
                return False
        except Exception as e:
            print(f"Error sending GET request: {e}")
            return False

    def send(self, command):
        """Основной метод отправки (использует POST)"""
        return self.send_post(command)


# Пример запуска отдельно для тестирования
if __name__ == "__main__":
    # Тестовая команда
    data = {
        "comman": "forward",
        "id": 33,
        "time": 1.00
    }

    sender = RESTSender()
    sender.send(data)