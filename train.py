import os
import pickle
import face_recognition
import numpy as np
from tqdm import tqdm  # Для прогресс-бара, установите pip install tqdm если нужно

# Путь к директории с известными персонами
KNOWN_PERSONS_DIR = './known_persons'
# Путь к файлу для сохранения encodings
PICKLE_FILE = 'known_persons.pkl'


def train_known_persons():
    known_face_encodings = []
    known_face_names = []

    # Собираем все фото для обработки
    all_images = []
    for person_name in os.listdir(KNOWN_PERSONS_DIR):
        person_dir = os.path.join(KNOWN_PERSONS_DIR, person_name)
        if not os.path.isdir(person_dir):
            continue
        for filename in os.listdir(person_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(person_dir, filename)
                all_images.append((image_path, person_name))

    # Обрабатываем с прогресс-баром
    for image_path, person_name in tqdm(all_images, desc="Обработка изображений"):
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if len(encodings) == 0:
                print(f"Нет лиц на изображении: {image_path}")
                continue
            elif len(encodings) > 1:
                print(f"Несколько лиц на изображении: {image_path}. Беру только первое.")
                # Можно добавить логику: пропустить или взять все, но для точности лучше одно лицо на фото

            # Добавляем encoding (как numpy array для совместимости)
            known_face_encodings.append(encodings[0])
            known_face_names.append(person_name)
        except Exception as e:
            print(f"Ошибка при обработке {image_path}: {e}")

    # Сохраняем в pickle файл
    data = {
        'names': known_face_names,
        'encodings': [np.array(enc) for enc in known_face_encodings]  # Преобразуем в numpy для лучшей совместимости
    }
    with open(PICKLE_FILE, 'wb') as f:
        pickle.dump(data, f)

    print(f"Обучение завершено. Сохранено {len(known_face_names)} encodings в {PICKLE_FILE}. "
          f"Из них уникальных персон: {len(set(known_face_names))}")


if __name__ == "__main__":
    train_known_persons()