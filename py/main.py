import cv2
import os

def decode_qr_code_cv2(image_path):
    """
    Декодирует QR-код из изображения

    Args:
        image_path (str): путь к изображению с QR-кодом

    Returns:
        str: декодированные данные или None
    """

    # Проверка существования файла
    if not os.path.exists(image_path):
        print(f"Файл не найден: {image_path}")
        print(f"Текущая директория: {os.getcwd()}")
        return None

    # Чтение изображения
    img = cv2.imread(image_path)

    # Проверка загрузки изображения
    if img is None:
        print(f"Не удалось загрузить изображение: {image_path}")
        print("Возможные причины:")
        print("  - Файл поврежден")
        print("  - Неподдерживаемый формат")
        return None

    print(f"Изображение загружено: {image_path}")
    print(f"   Размер: {img.shape[1]}x{img.shape[0]} пикселей")

    # Создание детектора QR-кодов
    detector = cv2.QRCodeDetector()

    # Детекция и декодирование
    data, bbox, straight_qrcode = detector.detectAndDecode(img)

    # Обработка результата
    if data:
        print(f"QR-код обнаружен!")
        print(f"Данные: {data}")

        # Рисуем рамку вокруг QR-кода (если нужно)
        if bbox is not None:
            for i in range(len(bbox[0])):
                pt1 = tuple(bbox[0][i].astype(int))
                pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])].astype(int))
                cv2.line(img, pt1, pt2, (0, 255, 0), 3)

            # Сохраняем изображение с рамкой
            output_path = "qr_with_bbox.jpg"
            cv2.imwrite(output_path, img)
            print(f"Изображение с рамкой сохранено: {output_path}")

        return data
    else:
        print("QR-код не обнаружен")
        return None

# Тестирование
if __name__ == "__main__":

    # Путь к файлу (измените на свой)
    image_path = "qr-code.png"

    # Полный путь для Windows
    # image_path = r"C:\Users\user\PycharmProjects\PythonProject4\my_qr_code.png"

    result = decode_qr_code_cv2(image_path)

    if result:
        print(f"\n  Декодированные данные: {result}")
    else:
        print("\n Не удалось декодировать QR-код")