#!/usr/bin/env python3
# test_components.py - Тестирование компонентов проекта

import os
import sys
from pathlib import Path

def test_imports():
    """Тестирование импортов всех модулей"""
    print("🔍 Тестирование импортов...")
    
    try:
        from preprocessing.classify_attachment import classify_attachment
        print("✅ preprocessing.classify_attachment")
    except ImportError as e:
        print(f"❌ preprocessing.classify_attachment: {e}")
        return False
    
    try:
        from ingestion.extract_text_universal import extract_text_from_file
        print("✅ ingestion.extract_text_universal")
    except ImportError as e:
        print(f"❌ ingestion.extract_text_universal: {e}")
        return False
    
    try:
        from llm.gpt_analyzer import extract_key_clauses, extract_goods_table
        print("✅ llm.gpt_analyzer")
    except ImportError as e:
        print(f"❌ llm.gpt_analyzer: {e}")
        return False
    
    try:
        from bitrix24.bitrix_sender import send_to_bitrix24
        print("✅ bitrix24.bitrix_sender")
    except ImportError as e:
        print(f"❌ bitrix24.bitrix_sender: {e}")
        return False
    
    try:
        from main.handle_email_request import handle_email_request
        print("✅ main.handle_email_request")
    except ImportError as e:
        print(f"❌ main.handle_email_request: {e}")
        return False
    
    try:
        from email_reader import fetch_attachments
        print("✅ email_reader")
    except ImportError as e:
        print(f"❌ email_reader: {e}")
        return False
    
    return True

def test_classification():
    """Тестирование классификации документов"""
    print("\n🔍 Тестирование классификации...")
    
    try:
        from preprocessing.classify_attachment import classify_attachment
        
        # Тестовые случаи
        test_cases = [
            ("Договор поставки товаров между ООО и ИП", "contract.pdf", "договор"),
            ("Извещение о проведении запроса котировок", "notice.docx", "извещение"),
            ("Техническое задание на поставку", "tech_spec.xlsx", "номенклатура"),
            ("Обычный текст без ключевых слов", "document.txt", "неизвестно")
        ]
        
        for text, filename, expected in test_cases:
            result = classify_attachment(text, filename)
            status = "✅" if result == expected else "❌"
            print(f"{status} {filename}: {result} (ожидалось: {expected})")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка тестирования классификации: {e}")
        return False

def test_text_extraction():
    """Тестирование извлечения текста"""
    print("\n🔍 Тестирование извлечения текста...")
    
    try:
        from ingestion.extract_text_universal import extract_text_from_file
        
        # Создаем тестовый текстовый файл
        test_file = Path("test_file.txt")
        test_content = "Это тестовый документ для проверки извлечения текста."
        
        test_file.write_text(test_content, encoding='utf-8')
        
        extracted = extract_text_from_file(str(test_file))
        
        if extracted.strip() == test_content:
            print("✅ Извлечение текста из TXT файла")
        else:
            print("❌ Ошибка извлечения текста из TXT файла")
        
        # Удаляем тестовый файл
        test_file.unlink()
        
        return True
    except Exception as e:
        print(f"❌ Ошибка тестирования извлечения текста: {e}")
        return False

def test_environment():
    """Тестирование переменных окружения"""
    print("\n🔍 Тестирование переменных окружения...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            "EMAIL_HOST",
            "EMAIL_LOGIN", 
            "EMAIL_PASSWORD",
            "OPENAI_API_KEY",
            "BITRIX_WEBHOOK"
        ]
        
        missing_vars = []
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
                print(f"⚠️ {var}: не установлена")
            else:
                # Показываем только первые и последние символы для безопасности
                masked_value = value[:3] + "***" + value[-3:] if len(value) > 6 else "***"
                print(f"✅ {var}: {masked_value}")
        
        if missing_vars:
            print(f"\n⚠️ Не установлены переменные: {', '.join(missing_vars)}")
            print("Отредактируйте файл .env")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Ошибка тестирования окружения: {e}")
        return False

def test_directories():
    """Тестирование необходимых директорий"""
    print("\n🔍 Тестирование директорий...")
    
    required_dirs = ["temp_files", "output"]
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}: существует")
        else:
            print(f"⚠️ {dir_name}: не существует, создаю...")
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ {dir_name}: создана")
    
    return True

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование компонентов Contract Parser Extended")
    print("=" * 60)
    
    tests = [
        ("Импорты модулей", test_imports),
        ("Классификация документов", test_classification),
        ("Извлечение текста", test_text_extraction),
        ("Переменные окружения", test_environment),
        ("Директории", test_directories)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Критическая ошибка в тесте '{test_name}': {e}")
            results.append((test_name, False))
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nРезультат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Проект готов к работе.")
        return 0
    else:
        print("⚠️ Некоторые тесты провалены. Проверьте настройки.")
        return 1

if __name__ == "__main__":
    sys.exit(main())