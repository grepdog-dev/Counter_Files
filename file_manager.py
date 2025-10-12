"""
Логика работы с файловой системой с поддержкой кириллицы
"""
import os
import logging
import shutil
import re
from pathlib import Path
from typing import List, Optional, Tuple


class FileManager:
    """Управление файловыми операциями с поддержкой кириллицы"""
    
    def __init__(self):
        self.selected_files: List[Tuple[Path, str]] = []
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        return logger
    
    def add_files(self, file_paths: List[str]) -> int:
        added_count = 0
        for file_path in file_paths:
            try:
                file_path_obj = Path(file_path)
                if file_path_obj.exists() and file_path_obj.is_file():
                    if not any(full_path == file_path_obj for full_path, _ in self.selected_files):
                        display_name = file_path_obj.name
                        self.selected_files.append((file_path_obj, display_name))
                        added_count += 1
            except Exception as e:
                self.logger.error(f"Ошибка добавления файла: {e}")
        return added_count
    
    def clear_files(self):
        self.selected_files.clear()
    
    def remove_file(self, index: int) -> bool:
        try:
            if 0 <= index < len(self.selected_files):
                self.selected_files.pop(index)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Ошибка удаления файла: {e}")
            return False
    
    def move_file_up(self, index: int) -> bool:
        if 0 < index < len(self.selected_files):
            self.selected_files[index], self.selected_files[index-1] = self.selected_files[index-1], self.selected_files[index]
            return True
        return False
    
    def move_file_down(self, index: int) -> bool:
        if 0 <= index < len(self.selected_files) - 1:
            self.selected_files[index], self.selected_files[index+1] = self.selected_files[index+1], self.selected_files[index]
            return True
        return False
    
    def rename_files(self, start_number: int, output_dir: Optional[Path] = None) -> Tuple[bool, int]:
        if not self.selected_files:
            return False, 0
        
        success_count = 0
        current_number = start_number
        
        try:
            for file_path, original_name in self.selected_files:
                if file_path.exists():
                    # Получаем чистое имя файла без существующей нумерации
                    clean_filename = self._remove_existing_numbering(file_path.name)
                    
                    # Создаем новое имя с номером
                    new_filename = f"{current_number}. {clean_filename}"
                    
                    if output_dir:
                        output_dir.mkdir(parents=True, exist_ok=True)
                        new_path = self._get_unique_filename(output_dir / new_filename)
                        shutil.copy2(file_path, new_path)
                    else:
                        new_path = self._get_unique_filename(file_path.parent / new_filename)
                        file_path.rename(new_path)
                    
                    success_count += 1
                    current_number += 1
                    self.logger.info(f"Файл переименован: {original_name} -> {new_filename}")
                    
            if success_count > 0:
                self.clear_files()
                
            return True, success_count
            
        except Exception as e:
            self.logger.error(f"Ошибка переименования: {e}")
            return False, success_count
    
    def _remove_existing_numbering(self, filename: str) -> str:
        """
        Удаляет существующую нумерацию из имени файла.
        
        Поддерживает форматы:
        - "1. filename.txt" -> "filename.txt"
        - "001_filename.jpg" -> "filename.jpg" 
        - "123- document.pdf" -> "document.pdf"
        - "1) file.name" -> "file.name"
        """
        # Паттерны для обнаружения нумерации в начале имени файла
        patterns = [
            # Формат: "число. пробел имя_файла"
            r'^\d+\.\s+(.*)$',
            # Формат: "число_имя_файла" 
            r'^\d+_(.*)$',
            # Формат: "число- пробел имя_файла"
            r'^\d+\-\s+(.*)$',
            # Формат: "число) пробел имя_файла"
            r'^\d+\)\s+(.*)$',
            # Формат: "число пробел имя_файла" (просто число и пробел)
            r'^\d+\s+(.*)$',
            # Формат: "число-имя_файла" (без пробела)
            r'^\d+\-(.*)$',
            # Формат: "число)имя_файла" (без пробела)
            r'^\d+\)(.*)$',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, filename)
            if match:
                clean_name = match.group(1)
                self.logger.info(f"Обнаружена нумерация в файле '{filename}' -> '{clean_name}'")
                return clean_name
        
        # Если нумерация не обнаружена, возвращаем оригинальное имя
        return filename
    
    def _get_unique_filename(self, file_path: Path) -> Path:
        """
        Генерирует уникальное имя файла, если файл с таким именем уже существует.
        """
        if not file_path.exists():
            return file_path
        
        counter = 1
        original_stem = file_path.stem
        extension = file_path.suffix
        parent_dir = file_path.parent
        
        while True:
            new_filename = f"{original_stem}_{counter}{extension}"
            new_path = parent_dir / new_filename
            if not new_path.exists():
                return new_path
            counter += 1
    
    def has_numbered_files(self) -> bool:
        """
        Проверяет, есть ли в списке файлы с существующей нумерацией.
        
        Returns:
            bool: True если есть пронумерованные файлы
        """
        for file_path, display_name in self.selected_files:
            if self._is_numbered_filename(display_name):
                return True
        return False
    
    def _is_numbered_filename(self, filename: str) -> bool:
        """
        Проверяет, содержит ли имя файла нумерацию в начале.
        
        Args:
            filename: Имя файла для проверки
            
        Returns:
            bool: True если файл уже пронумерован
        """
        patterns = [
            r'^\d+\.\s+',
            r'^\d+_',
            r'^\d+\-\s+',
            r'^\d+\)\s+',
            r'^\d+\s+',
            r'^\d+\-',
            r'^\d+\)',
        ]
        
        for pattern in patterns:
            if re.match(pattern, filename):
                return True
        return False
    
    def get_file_count(self) -> int:
        return len(self.selected_files)
    
    def get_display_names(self) -> List[str]:
        return [display_name for _, display_name in self.selected_files]
    
    def get_numbered_files_info(self) -> List[str]:
        """
        Возвращает информацию о файлах с существующей нумерацией.
        
        Returns:
            List[str]: Список строк с информацией о пронумерованных файлах
        """
        numbered_files = []
        for file_path, display_name in self.selected_files:
            if self._is_numbered_filename(display_name):
                clean_name = self._remove_existing_numbering(display_name)
                numbered_files.append(f"'{display_name}' -> '{clean_name}'")
        return numbered_files