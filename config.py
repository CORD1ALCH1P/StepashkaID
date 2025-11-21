import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Единая конфигурация приложения"""

    # Flask настройки
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', '5000'))

    # Настройки потока
    streaming_source = os.getenv('streaming_source', 'your source')
    streaming_height = int(os.getenv('streaming_height', '640'))
    streaming_width = int(os.getenv('streaming_width', '480'))


# Создаем экземпляр конфига
config = Config()