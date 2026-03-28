import cv2
import json
from datetime import datetime

class Recogniser:
    def __init__(self):
        # ������ ��� �������� ������� ���� ��������� QR-�����
        self.all_centers = []

    def calculate_center(self, points_dict):
        # ��������� ����� QR-����
        center_x = (points_dict['top_left'][0] + points_dict['top_right'][0] +
                    points_dict['bottom_right'][0] + points_dict['bottom_left'][0]) // 4
        center_y = (points_dict['top_left'][1] + points_dict['top_right'][1] +
                    points_dict['bottom_right'][1] + points_dict['bottom_left'][1]) // 4
        return [center_x, center_y]

    def scan_qr_codes(self):
        # ��������� ��������� QR-�����
        # ������������� ������
        cap = cv2.VideoCapture(0)

        # �������� ���������� �������� ������
        if not cap.isOpened():
            return None

        # �������� ��������� QR-�����
        detector = cv2.QRCodeDetector()

        # ������ ��� �������� ���� ���������� ��������� QR-�����
        scanned_codes = []
        # ������ ��� �������� ������� ������� QR-����
        centers_list = []

        while True:
            # ������ ����� � ������
            ret, frame = cap.read()

            # ������� ����� ��� ������ �������
            if not ret:
                continue

            # �������� ����� ����� ��� ���������
            display_frame = frame.copy()

            # ������������� ���� QR-����� �� �����
            retval, decoded_texts, points, straight_qrcode = detector.detectAndDecodeMulti(frame)

            # ���� ������� QR-����
            if retval and points is not None and len(points) > 0:
                # ����� ������� ���������� QR-����
                for i, (text, pts) in enumerate(zip(decoded_texts, points)):
                    if text:  # ���� ����� ������� �����������
                        # �������������� ��������� � ����� �����
                        pts = pts.astype(int)

                        # �������������� ����� � ������� � ���������� �����
                        points_dict = {
                            'top_left': [int(pts[0][0]), int(pts[0][1])],
                            'top_right': [int(pts[1][0]), int(pts[1][1])],
                            'bottom_right': [int(pts[2][0]), int(pts[2][1])],
                            'bottom_left': [int(pts[3][0]), int(pts[3][1])]
                        }

                        # ��������� ����� QR-����
                        center = self.calculate_center(points_dict)

                        # ��������� ������� ������� ������ QR-����
                        cv2.polylines(display_frame, [pts], True, (0, 255, 0), 2)

                        # ����������� ������� ����� � ������
                        cv2.circle(display_frame, (center[0], center[1]), 5, (0, 0, 255), -1)

                        # ���������� ������ QR-���� � ������
                        if text not in scanned_codes:
                            scanned_codes.append(text)
                            # ��������� ����� ��� ������� QR-����
                            centers_list.append(center)

                # ����������� �������� ��������� QR-�����
                cv2.putText(display_frame, f"Found: {len(scanned_codes)} QR codes",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # ����������� �����
            cv2.imshow('QR Scanner', display_frame)

            # ����� �� �����
            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('QR Scanner', cv2.WND_PROP_VISIBLE) < 1:
                break

        # ��������� ������ � ������� ������
        self.all_centers = centers_list

        # ������������ �������� ������
        cap.release()
        # �������� ���� ���� OpenCV
        cv2.destroyAllWindows()
        return scanned_codes

class FooQRRecogniser(Recogniser):
    # �����-��������� ��� ������������� � �������� QR-�����
    def recognise(self):
        # ���������� QR-���� � ����������� �� � ����������������� �������
        # ��������� ������ ��������� QR-�����
        codes = self.scan_qr_codes()

        if codes:
            results = []
            # ������� ������� ���������� QR-����
            for i, data in enumerate(codes):
                # �������� ����� ��� �������� QR-����
                current_center = self.all_centers[i] if i < len(self.all_centers) else []

                # ������� �����
                results.append({
                    'text': data,
                    'center': current_center  # ����� QR-����
                })
            return results
        return None

class FooSender:
    # ����� ��� �������� ������
    def send(self, command):
        # �������� ������� (� ������� ���������� ������ ���������� �������)
        return command

class AppServ:
    def __init__(self):
        # ������������� �����������
        self.recogniser = FooQRRecogniser()
        self.sender = FooSender()

    def run(self):
        # ������ ��������� ����� ����������
        # ������������� QR-�����
        commands = self.recogniser.recognise()

        if commands:
            # ���������� ������ ��� ����������
            json_data = {
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "qr_codes": commands
            }

            # ���������� ����������� � JSON ����
            with open("qr_result.json", "w", encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

            # �������� ������ �������
            for command in commands:
                self.sender.send(command)
        else:
            print("QR Code not detected or could not be decoded")

if __name__ == "__main__":
    app = AppServ()
    app.run()