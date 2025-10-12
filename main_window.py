"""
Главное окно приложения
"""
import logging
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QFileDialog, 
                             QCheckBox, QHBoxLayout, QVBoxLayout, QWidget,
                             QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

# Импортируем сгенерированный UI
from design_ui import Ui_MainWindow
from file_manager import FileManager


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        
        # Инициализация UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Инициализация менеджера файлов
        self.file_manager = FileManager()
        self.output_directory: Optional[Path] = None
        
        # Настройка интерфейса
        self._setup_ui()
        self._connect_signals()
        self._update_ui_state()
    
    def _setup_ui(self):
        """Настройка интерфейса"""
        self.setWindowTitle("Счётчик Файлов")
        
        # Скрываем ненужные элементы
        self.ui.btn_kat.setVisible(False)
        self.ui.lbl_kat.setVisible(False)
        
        # Обновляем текст
        self.ui.btn_fa.setText("Выберите Файлы")
        
        # Исправляем стиль spinBox
        self.ui.spinBox.setStyleSheet("")
        
        # Добавляем опции вывода
        self._add_output_options()
        
        # Добавляем информационную метку о нумерации
        self._add_numbering_info_label()
        
        # Настраиваем курсоры
        self._setup_cursors()
    
    def _add_output_options(self):
        """Добавление опций вывода"""
        # Создаем контейнер для опций вывода
        output_container = QWidget()
        output_layout = QVBoxLayout(output_container)
        
        # Создаем горизонтальный layout для чекбоксов
        checkbox_layout = QHBoxLayout()
        
        # Чекбокс для выбора папки вывода
        self.output_checkbox = QCheckBox("Сохранить в другую папку")
        self.output_button = QCheckBox("Выбрать папку для сохранения")
        self.output_button.setEnabled(False)
        
        checkbox_layout.addWidget(self.output_checkbox)
        checkbox_layout.addWidget(self.output_button)
        checkbox_layout.addStretch()
        
        output_layout.addLayout(checkbox_layout)
        output_layout.setContentsMargins(50, 10, 50, 10)
        
        # Добавляем в интерфейс
        try:
            output_container.setParent(self.ui.centralwidget)
            output_container.setGeometry(50, 500, 400, 60)
        except Exception as e:
            logging.error(f"Ошибка при добавлении опций вывода: {e}")
    
    def _add_numbering_info_label(self):
        """Добавляет метку для информации о нумерации"""
        self.numbering_info_label = QLabel("", self.ui.centralwidget)
        self.numbering_info_label.setGeometry(50, 570, 600, 30)
        self.numbering_info_label.setStyleSheet("color: blue; font-size: 12px;")
        self.numbering_info_label.setVisible(False)
    
    def _setup_cursors(self):
        """Настройка курсоров"""
        pointing_cursor = QCursor(Qt.PointingHandCursor)
        buttons = [
            self.ui.btn_och, self.ui.btn_fa, self.ui.btn_pre, 
            self.ui.btn_up, self.ui.btn_down, self.ui.btn_del
        ]
        for button in buttons:
            button.setCursor(pointing_cursor)
    
    def _connect_signals(self):
        """Подключение сигналов"""
        # Основные кнопки
        self.ui.btn_och.clicked.connect(self._on_clear_list)
        self.ui.btn_fa.clicked.connect(self._on_select_files)
        self.ui.btn_pre.clicked.connect(self._on_rename_files)
        self.ui.btn_up.clicked.connect(self._on_move_up)
        self.ui.btn_down.clicked.connect(self._on_move_down)
        self.ui.btn_del.clicked.connect(self._on_delete_selected)
        
        # Список файлов
        self.ui.list.currentRowChanged.connect(self._on_selection_changed)
        
        # Опции вывода
        self.output_checkbox.toggled.connect(self._on_output_checkbox_toggled)
        self.output_button.clicked.connect(self._on_select_output_directory)
    
    def _on_output_checkbox_toggled(self, checked):
        """Обработчик переключения чекбокса вывода"""
        self.output_button.setEnabled(checked)
        if not checked:
            self.output_directory = None
            self.output_button.setText("Выбрать папку для сохранения")
    
    def _on_select_output_directory(self):
        """Обработчик выбора директории вывода"""
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Выберите папку для сохранения переименованных файлов"
        )
        
        if directory:
            self.output_directory = Path(directory)
            display_path = str(self.output_directory)
            if len(display_path) > 40:
                display_path = "..." + display_path[-37:]
            self.output_button.setText(f"Папка: {display_path}")
    
    def _on_select_files(self):
        """Обработчик выбора файлов"""
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            "Выберите файлы для переименования",
            "",
            "Все файлы (*.*)"
        )
        
        if files:
            added_count = self.file_manager.add_files(files)
            if added_count > 0:
                self._refresh_list_display()
                self._update_ui_state()
                self._update_numbering_info()
                self._show_info(f"Добавлено файлов: {added_count}")
            else:
                self._show_warning("Не удалось добавить файлы или они уже в списке")
    
    def _update_numbering_info(self):
        """Обновляет информацию о нумерации файлов"""
        if self.file_manager.has_numbered_files():
            numbered_files = self.file_manager.get_numbered_files_info()
            info_text = f"Обнаружены файлы с нумерацией: {len(numbered_files)} файл(ов) будут переименованы"
            if len(numbered_files) <= 3:  # Показываем детали только для небольшого количества файлов
                details = "; ".join(numbered_files)
                info_text += f" ({details})"
            
            self.numbering_info_label.setText(info_text)
            self.numbering_info_label.setVisible(True)
        else:
            self.numbering_info_label.setVisible(False)
    
    def _on_clear_list(self):
        """Обработчик очистки списка"""
        self.file_manager.clear_files()
        self.ui.list.clear()
        self._update_ui_state()
        self.numbering_info_label.setVisible(False)
    
    def _on_rename_files(self):
        """Обработчик переименования файлов"""
        if self.file_manager.get_file_count() == 0:
            self._show_warning("Нет файлов для переименования!")
            return
        
        start_number = self.ui.spinBox.value()
        
        # Проверяем, нужно ли сохранять в другую папку
        output_dir = None
        if self.output_checkbox.isChecked():
            if not self.output_directory:
                self._show_warning("Сначала выберите папку для сохранения!")
                return
            output_dir = self.output_directory
        
        # Показываем подтверждение для файлов с существующей нумерацией
        if self.file_manager.has_numbered_files():
            reply = QMessageBox.question(
                self,
                "Подтверждение переименования",
                "Обнаружены файлы с существующей нумерацией. "
                "Старая нумерация будет заменена на новую. Продолжить?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        success, count = self.file_manager.rename_files(start_number, output_dir)
        
        if success:
            self._show_info(f"Успешно переименовано {count} файлов!")
            self.ui.list.clear()
            self._update_ui_state()
            self.numbering_info_label.setVisible(False)
        else:
            if count > 0:
                self._show_warning(f"Частично выполнено! Обработано {count} файлов, но возникли ошибки")
            else:
                self._show_error("Не удалось переименовать файлы!")
    
    def _on_move_up(self):
        """Перемещение файла вверх"""
        current_row = self.ui.list.currentRow()
        if self.file_manager.move_file_up(current_row):
            self._refresh_list_display()
            new_index = max(0, current_row - 1)
            self.ui.list.setCurrentRow(new_index)
    
    def _on_move_down(self):
        """Перемещение файла вниз"""
        current_row = self.ui.list.currentRow()
        if self.file_manager.move_file_down(current_row):
            self._refresh_list_display()
            new_index = min(self.ui.list.count() - 1, current_row + 1)
            self.ui.list.setCurrentRow(new_index)
    
    def _on_delete_selected(self):
        """Удаление выбранного файла"""
        current_row = self.ui.list.currentRow()
        if self.file_manager.remove_file(current_row):
            self.ui.list.takeItem(current_row)
            self._update_ui_state()
            self._update_numbering_info()
    
    def _on_selection_changed(self, current_row):
        """Обработчик изменения выбора"""
        self._update_buttons_state(current_row)
    
    def _refresh_list_display(self):
        """Обновление отображения списка"""
        self.ui.list.clear()
        for display_name in self.file_manager.get_display_names():
            self.ui.list.addItem(display_name)
    
    def _update_ui_state(self):
        """Обновление состояния UI"""
        file_count = self.file_manager.get_file_count()
        current_row = self.ui.list.currentRow()
        
        # Обновляем информацию о файлах
        self.ui.lbl_fayl.setText(f"Ваши файлы: {file_count}")
        
        # Обновляем кнопки
        has_files = file_count > 0
        self.ui.btn_pre.setEnabled(has_files)
        self.ui.btn_och.setEnabled(has_files)
        self._update_buttons_state(current_row)
    
    def _update_buttons_state(self, current_row):
        """Обновление состояния кнопок"""
        file_count = self.file_manager.get_file_count()
        has_valid_selection = 0 <= current_row < file_count
        
        self.ui.btn_up.setEnabled(has_valid_selection and current_row > 0)
        self.ui.btn_down.setEnabled(has_valid_selection and current_row < file_count - 1)
        self.ui.btn_del.setEnabled(has_valid_selection)
    
    def _show_info(self, message):
        QMessageBox.information(self, "Информация", message)
    
    def _show_warning(self, message):
        QMessageBox.warning(self, "Предупреждение", message)
    
    def _show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)