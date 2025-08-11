#!/usr/bin/env python3
# setup.py - Скрипт настройки проекта

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Установка зависимостей из requirements.txt"""
    print("📦 Установка зависимостей...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Зависимости установлены успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки зависимостей: {e}")
        return False

def create_env_file():
    """Создание .env файла из шаблона"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️ Файл .env уже существует")
        return True
    
    if not env_example.exists():
        print("❌ Файл .env.example не найден")
        return False
    
    try:
        env_file.write_text(env_example.read_text(encoding='utf-8'), encoding='utf-8')
        print("✅ Создан файл .env из шаблона")
        print("📝 Не забудьте отредактировать .env с вашими настройками!")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания .env: {e}")
        return False

def create_directories():
    """Создание необходимых директорий"""
    dirs = ["temp_files", "output", "logs"]
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Создана директория: {dir_name}")
    
    return True

def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        print(f"Текущая версия: {sys.version}")
        return False
    
    print(f"✅ Python версия: {sys.version}")
    return True

def main():
    """Основная функция настройки"""
    print("🚀 Настройка проекта Contract Parser Extended")
    print("=" * 50)
    
    # Проверка версии Python
    if not check_python_version():
        sys.exit(1)
    
    # Создание директорий
    if not create_directories():
        print("❌ Ошибка создания директорий")
        sys.exit(1)
    
    # Создание .env файла
    if not create_env_file():
        print("❌ Ошибка создания .env файла")
        sys.exit(1)
    
    # Установка зависимостей
    if not install_requirements():
        print("❌ Ошибка установки зависимостей")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Настройка завершена успешно!")
    print("\n📝 Следующие шаги:")
    print("1. Отредактируйте файл .env с вашими настройками")
    print("2. Запустите: python run_scheduled.py")
    print("3. Для автоматического запуска настройте планировщик заданий")
    print("\n📖 Подробности в README.md")

if __name__ == "__main__":
    main()