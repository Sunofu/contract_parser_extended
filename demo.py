#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрационный скрипт для тестирования функциональности contract_parser_extended
"""

import os
import json
from pathlib import Path

# Импорт модулей проекта
from preprocessing.classify_attachment import classify_attachment
from ingestion.extract_text_universal import extract_text_from_file
from llm.gpt_analyzer import extract_key_clauses, extract_goods_table
from main.handle_email_request import handle_email_request

def create_test_files():
    """Создание тестовых файлов для демонстрации"""
    test_dir = Path("temp_files")
    test_dir.mkdir(exist_ok=True)
    
    # Создаем тестовый договор
    contract_content = """
    ДОГОВОР ПОСТАВКИ № 123/2024
    
    Поставщик: ООО "Тест Поставщик"
    Покупатель: ООО "Тест Покупатель"
    
    Предмет договора: Поставка товаров согласно спецификации
    Сумма договора: 1 000 000 рублей
    Срок поставки: до 31.12.2024
    
    Условия оплаты: 100% предоплата
    """
    
    contract_file = test_dir / "test_contract.txt"
    with open(contract_file, 'w', encoding='utf-8') as f:
        f.write(contract_content)
    
    # Создаем тестовое извещение
    notice_content = """
    ИЗВЕЩЕНИЕ О ПРОВЕДЕНИИ ТЕНДЕРА № 456/2024
    
    Организатор: Государственное учреждение
    Предмет закупки: Поставка канцелярских товаров
    Начальная цена: 500 000 рублей
    Срок подачи заявок: до 15.01.2025
    """
    
    notice_file = test_dir / "test_notice.txt"
    with open(notice_file, 'w', encoding='utf-8') as f:
        f.write(notice_content)
    
    return [str(contract_file), str(notice_file)]

def demo_classification():
    """Демонстрация классификации документов"""
    print("=" * 60)
    print("🔍 ДЕМОНСТРАЦИЯ КЛАССИФИКАЦИИ ДОКУМЕНТОВ")
    print("=" * 60)
    
    test_files = create_test_files()
    
    for file_path in test_files:
        filename = os.path.basename(file_path)
        text = extract_text_from_file(file_path)
        classification = classify_attachment(text, filename)
        
        print(f"📄 Файл: {filename}")
        print(f"📝 Содержимое: {text[:100]}...")
        print(f"🏷️  Классификация: {classification}")
        print("-" * 40)

def demo_text_extraction():
    """Демонстрация извлечения текста"""
    print("=" * 60)
    print("📖 ДЕМОНСТРАЦИЯ ИЗВЛЕЧЕНИЯ ТЕКСТА")
    print("=" * 60)
    
    test_files = create_test_files()
    
    for file_path in test_files:
        filename = os.path.basename(file_path)
        text = extract_text_from_file(file_path)
        
        print(f"📄 Файл: {filename}")
        print(f"📝 Извлеченный текст ({len(text)} символов):")
        print(text)
        print("-" * 40)

def demo_full_pipeline():
    """Демонстрация полного пайплайна обработки"""
    print("=" * 60)
    print("⚙️ ДЕМОНСТРАЦИЯ ПОЛНОГО ПАЙПЛАЙНА")
    print("=" * 60)
    
    test_files = create_test_files()
    
    for file_path in test_files:
        print(f"🔄 Обработка файла: {os.path.basename(file_path)}")
        
        try:
            # Запускаем полный пайплайн
            result = handle_email_request([file_path])
            
            if result:
                print("✅ Файл успешно обработан")
                print("📋 Результат обработки:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
                
                # Проверяем, создался ли файл результата
                output_file = "output/email_parsed.json"
                if os.path.exists(output_file):
                    print(f"📊 Результат также сохранен в файл: {output_file}")
            else:
                print("❌ Ошибка обработки файла")
                
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        
        print("-" * 40)

def main():
    """Главная функция демонстрации"""
    print("🚀 ДЕМОНСТРАЦИЯ CONTRACT_PARSER_EXTENDED")
    print("=" * 60)
    
    # Проверяем наличие необходимых директорий
    for dir_name in ["temp_files", "output", "logs"]:
        Path(dir_name).mkdir(exist_ok=True)
    
    try:
        # Демонстрация классификации
        demo_classification()
        
        # Демонстрация извлечения текста
        demo_text_extraction()
        
        # Демонстрация полного пайплайна
        demo_full_pipeline()
        
        print("=" * 60)
        print("✅ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Ошибка демонстрации: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()