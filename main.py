"""
Точка входа в приложение
"""
import sys
import os
import logging

# Настройка HighDPI ДО создания приложения
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_window import MainWindow


def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('file_counter.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def main():
    """Основная функция приложения"""
    # Настройка HighDPI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Создание приложения
    app = QApplication(sys.argv)
    
    # Настройка логирования
    setup_logging()
    
    # Создание и отображение главного окна
    window = MainWindow()
    window.show()
    
    # Запуск главного цикла
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()