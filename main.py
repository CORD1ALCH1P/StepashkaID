import face_recognition
from face_recognition import face_locations

import WebGUI
# import cv2
# from config import *
# import simple_facerec
# from simple_facerec import simple_facerec
#
# # encode faces from a folder
# sfr = simple_facerec()
# sfr.load_encoding_images("./known_faces/test_person/")
#
#
# # camera
# cap = cv2.VideoCapture(config.streaming_source)
#
# while True:
#     ret, frame = cap.read()
#
#     # detect faces
#     face_locations, face_names = sfr.detect_known_faces(frame)
#     for fac_loc, name in zip(face_locations, face_names):
#         print(fac_loc)
#
#     cv2.imshow('frame',frame)
#
#     key = cv2.waitKey(1)
#     if key == 27:
#         break
#
# cap.release()
# cv2.destroyAllWindows()

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.streaming_width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.streaming_height)
# os.environ['QT_QPA_PLATFORM'] = 'offscreen'
#
# img = cv2.imread("./known_faces/test_person/1.jpg")
# rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img_encoding = face_recognition.face_encodings(rgb_img)[0]
#
# img2 = cv2.imread("./known_faces/test_person/2.jpg")
# rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
# img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]
#
# result = face_recognition.compare_faces([img_encoding], img_encoding2)
# print("Result: ", result)

# cv2.imshow("Img", img)
# cv2.waitKey(0)

import config
import face_recognition
import cv2
import numpy as np
import os
from config import Config
setting = Config()
import time


class SimpleFaceRec:
    def __init__(self):
        self.known_face_encodings = []

    def load_encoding_images(self, images_path):
        """Загрузка известных лиц"""
        try:
            for image_name in os.listdir(images_path):
                if image_name.endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(images_path, image_name)
                    print(f"Загрузка {image_name}...")

                    img = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(img)

                    if encodings:
                        self.known_face_encodings.append(encodings[0])
                        print(f"  ✓ Лицо найдено и закодировано")
                    else:
                        print(f"  ✗ Лица не найдено на изображении")

            print(f"Итог: Загружено {len(self.known_face_encodings)} известных лиц")

        except Exception as e:
            print(f"Ошибка при загрузке изображений: {e}")

    def check_for_known_faces(self, frame):
        """Проверяет, есть ли известные лица в кадре"""
        try:
            # Конвертируем BGR в RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Сначала находим все лица в кадре
            face_locations = face_recognition.face_locations(rgb_frame)

            if not face_locations:
                return False, 0  # Лица не обнаружены

            # Получаем кодировки для найденных лиц
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            known_faces_count = 0
            # Проверяем каждое найденное лицо
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                if True in matches:
                    known_faces_count += 1

            return known_faces_count > 0, len(face_locations)

        except Exception as e:
            print(f"Ошибка при распознавании: {e}")
            return False, 0


# Основной код
def main():
    sfr = SimpleFaceRec()

    # Проверяем существование папки
    if not os.path.exists("./known_faces/test_person/"):
        print("Ошибка: Папка ./known_faces/test_person/ не существует!")
        return

    sfr.load_encoding_images("./known_faces/test_person/")

    # Проверяем, есть ли загруженные лица
    if len(sfr.known_face_encodings) == 0:
        print("Предупреждение: Не загружено ни одного известного лица!")
        print("Добавьте изображения в папку ./known_faces/test_person/")

    cap = cv2.VideoCapture(0)

    # Проверяем, открылась ли камера
    if not cap.isOpened():
        print("Ошибка: Не удалось открыть камеру!")
        return

    print("\nЗапуск проверки лиц...")
    print("Нажмите Ctrl+C для выхода")
    print("-" * 40)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Ошибка чтения кадра с камеры")
                break

            # Проверяем наличие известных лиц
            known_face_detected, total_faces = sfr.check_for_known_faces(frame)

            # Выводим результат
            status = "TRUE" if known_face_detected else "FALSE"
            print(f"Лиц в кадре: {total_faces} | Известное лицо: {status}")

            # Задержка 1 секунда
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nОстановка...")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
    finally:
        cap.release()
        print("Камера освобождена")


if __name__ == "__main__":
    main()