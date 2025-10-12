"""
Константы и настройки приложения
"""

class AppConfig:
    """Конфигурация приложения"""
    APP_NAME = "Счётчик Файлов"
    WINDOW_WIDTH = 1119
    WINDOW_HEIGHT = 787
    DEFAULT_START_NUMBER = 1
    
    # Стили
    BUTTON_STYLE = """
    QPushButton{
        background-color: rgb(234, 234, 234);
        border: 3px solid rgb(167, 167, 167);
    }
    """
    
    # Сообщения
    SUCCESS_RENAME = "Файлы успешно переименованы!"
    ERROR_ACCESS = "Ошибка доступа к файлу: {}"
    WARNING_NO_FILES = "Нет файлов для переименования!"
    INFO_FILES_ADDED = "Добавлено файлов: {}"
    
    # Настройки кодировки
    SUPPORTED_ENCODINGS = ['utf-8', 'cp1251', 'koi8-r']