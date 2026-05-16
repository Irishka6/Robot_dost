import cv2
import json
from datetime import datetime

class Recogniser:
    def __init__(self):
        # Список для хранения центров всех найденных QR-кодов
        self.all_centers = []

    def calculate_center(self, points_dict):
        # Вычисляет центр QR-кода
        center_x = (points_dict['top_left'][0] + points_dict['top_right'][0] +
                    points_dict['bottom_right'][0] + points_dict['bottom_left'][0]) // 4
        center_y = (points_dict['top_left'][1] + points_dict['top_right'][1] +
                    points_dict['bottom_right'][1] + points_dict['bottom_left'][1]) // 4
        return [center_x, center_y]

    def scan_qr_codes(self):
        # Сканирует несколько QR-кодов
        # Инициализация камера
        cap = cv2.VideoCapture(0)

        # Проверка успешности открытия камеры
        if not cap.isOpened():
            return None

        # Создание детектора QR-кодов
        detector = cv2.QRCodeDetector()

        # Список для хранения всех уникальных считанных QR-кодов
        scanned_codes = []
        # Список для хранения центров каждого QR-кода
        centers_list = []

        while True:
            # Захват кадра с камеры
            ret, frame = cap.read()

            # Пропуск кадра при ошибке захвата
            if not ret:
                continue

            # Создание копии кадра для отрисовки
            display_frame = frame.copy()

            # Декодирование всех QR-кодов на кадре
            retval, decoded_texts, points, straight_qrcode = detector.detectAndDecodeMulti(frame)

            # Если найдены QR-коды
            if retval and points is not None and len(points) > 0:
                # Обход каждого найденного QR-кода
                for i, (text, pts) in enumerate(zip(decoded_texts, points)):
                    if text:  # Если текст успешно декодирован
                        # Преобразование координат в целые числа
                        pts = pts.astype(int)

                        # Преобразование точек в словарь с названиями углов
                        points_dict = {
                            'top_left': [int(pts[0][0]), int(pts[0][1])],
                            'top_right': [int(pts[1][0]), int(pts[1][1])],
                            'bottom_right': [int(pts[2][0]), int(pts[2][1])],
                            'bottom_left': [int(pts[3][0]), int(pts[3][1])]
                        }

                        # Вычисляем центр QR-кода
                        center = self.calculate_center(points_dict)

                        # Отрисовка зеленой границы вокруг QR-кода
                        cv2.polylines(display_frame, [pts], True, (0, 255, 0), 2)

                        # Отображение красной точки в центре
                        cv2.circle(display_frame, (center[0], center[1]), 5, (0, 0, 255), -1)

                        # Добавление нового QR-кода в список
                        if text not in scanned_codes:
                            scanned_codes.append(text)
                            # Сохраняем центр для каждого QR-кода
                            centers_list.append(center)

                # Отображение счетчика найденных QR-кодов
                cv2.putText(display_frame, f"Found: {len(scanned_codes)} QR codes",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Отображение кадра
            cv2.imshow('QR Scanner', display_frame)

            # Выход из цикла
            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('QR Scanner', cv2.WND_PROP_VISIBLE) < 1:
                break

        # Сохраняем центры в атрибут класса
        self.all_centers = centers_list

        # Освобождение ресурсов камеры
        cap.release()
        # Закрытие всех окон OpenCV
        cv2.destroyAllWindows()
        return scanned_codes


class FooQRRecogniser(Recogniser):
    # Класс-наследник для распознавания и парсинга QR-кодов
    def recognise(self):
        # Распознает QR-коды и преобразует их в структурированные команды
        # Получение списка считанных QR-кодов
        codes = self.scan_qr_codes()

        if codes:
            results = []
            # Парсинг каждого считанного QR-кода
            for i, data in enumerate(codes):
                # Получаем центр для текущего QR-кода
                current_center = self.all_centers[i] if i < len(self.all_centers) else []

                # Обычный текст
                results.append({
                    'text': data,
                    'center': current_center  # Центр QR-кода
                })
            return results
        return None


# Базовый класс для отправки команд (может быть переопределен)
class FooSender:
    def send(self, command):
        return command


class AppServ:
    def __init__(self, sender=None):
        # Инициализация компонентов
        self.recogniser = FooQRRecogniser()
        self.sender = sender if sender else FooSender()

    def run(self):
        # Запуск основного цикла приложения
        # Распознавание QR-кодов
        commands = self.recogniser.recognise()

        if commands:
            # Подготовка данных для сохранения
            json_data = {
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "qr_codes": commands
            }

            # Сохранение результатов в JSON файл
            with open("qr_result.json", "w", encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

            # Отправка каждой команды
            for i, command in enumerate(commands):
                # Преобразование в команду для робота
                robot_command = self.parse_qr_to_command(command['text'], i)
                self.sender.send(robot_command)
        else:
            print("QR Code not detected or could not be decoded")

    def parse_qr_to_command(self, qr_text, index):
        # Преобразование текста QR-кода в команду для робота
        if ':' in qr_text:
            cmd, time_val = qr_text.split(':')
            return {
                "comman": cmd,
                "id": index,
                "time": float(time_val)
            }
        else:
            return {
                "comman": qr_text,
                "id": index,
                "time": 1.0
            }


if __name__ == "__main__":
    app = AppServ()
    app.run()